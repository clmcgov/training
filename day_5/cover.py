'''
Image processing module for calculating cover from tetracam images

Band order is not valid in general -- this is for reformatted images. Bands must
be conformed to this order, and images must be foramatted as 6-page tifs where
each page is a band as a true monochrome image (not RGB with identical values).

contact: cullen.mcgovern@usda.gov
'''

from math import ceil, sqrt
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path
from pdb import set_trace

from PIL import Image, ImageSequence
from numpy import arange, array, divide, dstack, float32, int16, isfinite, random
from pandas import Timestamp, DataFrame, concat
from skimage.filters import threshold_otsu

BANDS = ('nir', 'edge', 'red', 'yellow', 'green', 'blue')

def proc_dir(path):
    '''process a directory of tetramcam images in a parallel


    Parameters
    ----------
    path : str or pathlib.Path
        path to image directory

    Returns
    -------
    DataFrame
    '''
    imgs = tuple(Path(path).iterdir())
    # get number of processors
    nproc = cpu_count()
    # evenly distribute images, with a single process and task per chunk
    size = ceil(len(imgs) / nproc)
    with Pool(nproc) as pool:
        # collect results in a dataframe
        res = concat(pool.imap_unordered(proc_img, imgs, chunksize=size))
    return res.sort_index()

def proc_img(path):
    '''process a tetracam image file formatted as date_plot[.ext]


    Parameters
    ----------
    path : str or pathlib.Path


    Returns
    -------
    DataFrame
    '''
    path = Path(path)
    # get image identifiers
    date, plot = parse_name(path)
    # open image in context manager (ensure closure)
    with Image.open(path) as img:
        # it's a multipage tif, we want to access bands by index
        mtif = ImageSequence.Iterator(img)
        # extract m x n x 2 array
        nir = array(mtif[BANDS.index('nir')])
        red = array(mtif[BANDS.index('red')])
    # get fake ndvi once for entire image
    a = ndvi(nir, red)
    # list of canopy cover for each sample
    cc = [otsu(s) for s in sample(a)]
    # create dataframe with identifiers, assign rep numbers to each sample
    df = DataFrame({'date': date, 'plot': plot, 'cc': cc,
        'rep': range(len(cc))})
    return df.set_index(['date', 'plot', 'rep'])

def sample(a):
    '''take 10 square random samples of 10% of the image each


    Parameters
    ----------
    a : ndarray
        array to sample


    Returns
    -------
    list
    '''
    # original image dimensions
    y, x = a.shape
    # dimension of sqare
    s = int(sqrt(0.1 * y * x))
    # generate a window of indices over a flattened image
    idxr = arange(s)[None, :] + x * arange(s)[:, None]
    # seed indices -- prevent index errors and overflows
    idxs = random.randint(0, x - s, 10) \
        + x * random.randint(0, y - s, 10)
    # flatten to index
    a = a.flatten()
    # add each idx to idxr, index image
    return [a[idxr + idx] for idx in idxs]

def parse_name(path):
    '''extract plot id and date from image name


    Parameters
    ----------
    path : str or pathlib.Path
        path to image


    Returns
    -------
    pandas.Timestamp, str
    '''
    date, plot = path.stem.split('_')
    return Timestamp(date), plot

def ndvi(nir, red):
    '''calculate NDVI


    Parameters
    ----------
    nir : ndarray
        nir band
    red : ndarray
        red band


    Returns
    -------
    numpy.array
    '''
    # must be signed and larger than 255
    nir, red = nir.astype(int16), red.astype(int16)
    return (nir - red) / (nir + red)

def otsu(a):
    '''get fractional canopy cover using Otsu's method


    Parameters
    ----------
    a : ndarray
        array of ndvi results


    Returns
    -------
    float
    '''
    a = a[isfinite(a)]
    # get threshold using otsu's method
    th = threshold_otsu(a)
    # pixels greater than the threshold are 1 (true), below are 0
    return (a > th).sum() / a.size

def rgb(path, r='red', g='green', b='blue'):
    '''generate an RGB image, optionally reassigning bands


    Parameters
    ----------
    path : str or pathlib.Path
        path to image
    r : str
        band to display as red
    g : str
        band to display as green
    b : str
        band to display as blue


    Returns
    -------
    PIL.Image


    Notes
    -----
    The returned Image object has all of the methods needed for saving, showing,
    etc.
    '''
    with Image.open(path) as img:
        mtif = ImageSequence.Iterator(img)
        return Image.merge(mode='RGB',
            bands=(mtif[self.BANDS.index(b)] for b in (r, g, b)))
