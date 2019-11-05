from math import ceil
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path

from PIL import Image, ImageSequence
from pandas import DataFrame, Timestamp
from numpy import array, float32, int16, isfinite, uint8, where
from skimage.filters import threshold_otsu

# image bands in order (2019 only)
BANDS = ('nir', 'blue', 'green', 'yellow', 'red', 'edge')

def get_band(mtif, name):
    '''get a band by name from a tetracam multi-tiff


    Parameters
    ----------
    mtif: PIL.ImageSequence
    name: str
        one of (nir, blue, green, yellow, red, edge)


    Returns
    -------
    PIL.Image
    '''
    return mtif[BANDS.index(name)].getchannel(0)

def img_to_cover(path):
    '''calculate canopy cover from a tetracam multi-tiff file (2019 only)


    Parameters
    ----------
    path: str or pathlib.Path


    Returns
    -------
    float
    '''
    img = Image.open(path) # get image file object
    mtif = ImageSequence.Iterator(img) # it's a multi-tiff
    res = ndvi( # get NDVI, don't keep bands in memory
        nir=array(get_band(mtif, 'nir')),
        red=array(get_band(mtif, 'red')))
    res = res[isfinite(res)] # remove nan/inf
    th = threshold_otsu(res) # get threshold
    res = where(res > th, 1, 0).astype(uint8) # classify
    return res.sum() / res.size # get scalar c

def mproc_img_dir(path, nproc=None):
    '''process a directory of tetramcam images in a parallel


    Parameters
    ----------
    path: str or pathlib.Path
    nproc: int, default None
        maximum number of processes


    Returns
    -------
    pandas.DataFrame
    '''
    imgs = list(Path(path).iterdir()) # to get length -- shouldn't be that big
    cpus = cpu_count() - 1  # save one for the OS
    if nproc and nproc < cpus: # if limit specified and we're over
        cpus = nproc # drop down to limit
    chunksize = ceil(len(imgs) / cpus) # images per process, round up
    with Pool(cpus) as pool: # set up process pool in context manager
        tmp = pool.imap_unordered(proc_img, imgs, chunksize) # lazy version
        df = DataFrame(tmp, columns=['date', 'plot', 'cover'])
    return df.set_index(['date', 'plot']).sort_index()

def ndvi(nir, red):
    '''calculate normalized difference vegetation index (NDVI)


    Parameters
    ----------
    nir: numpy.array
        near-infrared band
    red: numpy.array
        red band


    Returns
    -------
    numpy.array
    '''
    # must be signed and larger than 255
    red, nir = red.astype(int16), nir.astype(int16)
    return ((nir - red) / (nir + red)).astype(float32)

def proc_img(path):
    '''process a tetracam image file formatted as date_plot[.ext]


    file name format: 'date_plot.ext'


    Parameters
    ----------
    path: str or pathlib.Path


    Returns
    -------
    pandas.Timestamp
        image timestamp
    str
        image location
    float
        canopy cover
    '''
    date, plot = path.stem.split('_') # break up file name, sans extension
    date = Timestamp(date) # pandas should be able to read it
    cover = img_to_cover(path) # get cover
    return date, plot, cover

def proc_img_dir(path):
    '''process a directory of tetracam images in a single process


    Parameters
    ----------
    path: str or pathlib.Path


    Returns
    -------
    pandas.DataFrame
    '''
    path = Path(path)
    res = (proc_img(p) for p in path.iterdir()) # as generator
    res = DataFrame(res, columns=['date', 'plot', 'cover'])
    return res.set_index(['date', 'plot'])

def show_rgb(mtif, r='red', g='green', b='blue'):
    '''show an RGB image, optionally reassigning bands


    Parameters
    ----------
    mtif: PIL.ImageSequence
    r: str
        band to display as red
    g: str
        band to display as green
    b: str
        band to display as blue


    Notes
    -----
    available bands: (nir, blue, green, yellow, red, edge)
    '''
    img = Image.merge(
        mode='RGB',
        bands=(
            get_band(mtif, r),
            get_band(mtif, g),
            get_band(mtif, b)))
    img.show()

if __name__ == '__main__':
    from sys import argv
    try:
        path = argv[1]
    except IndexError:
        print('provide an image directory')
        exit()
    try:
        name = argv[2]
    except IndexError:
        print('provide an output file')
        exit()
    mproc_img_dir(path).to_csv(name)
