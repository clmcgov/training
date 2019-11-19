from math import ceil
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path

from PIL import Image, ImageSequence
from pandas import DataFrame, Timestamp
from numpy import array, float32, int16, isfinite, uint8, where
from skimage.filters import threshold_otsu

# image bands (sorted by frequency)
BANDS = ('nir', 'edge', 'red', 'yellow', 'green', 'blue')

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


def img_to_cc(path):
    '''calculate canopy cover from a tetracam multi-tiff file (2019 only)

    Parameters
    ----------
    path: str or pathlib.Path


    Returns
    -------
    float


    >>> img_to_cc('images/10jul2019_A11.tif').round(2)
    0.13
    '''
    # get image file object
    with Image.open(path) as img:
        # it's a multipage tiff, we want to access bands by index
        mtif = ImageSequence.Iterator(img)
        # get NDVI, don't keep bands in memory
        res = ndvi(
            nir=array(mtif[BANDS.index('nir')]),
            red=array(mtif[BANDS.index('red')]))
        # remove nan/inf
    res = res[isfinite(res)]
    # get threshold using otsu's method
    th = threshold_otsu(res)
    # pixels greater than the threshold are 1 (true), below are 0
    return (res > th).sum() / res.size

def proc_img(path):
    '''process a tetracam image file formatted as date_plot[.ext]


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


    Notes
    -----

    To parse the filenames, we'll first get the stem of the path object -- the
    filename with no extension. We can use the string split method with multiple
    assignment to extract the information.

    >>> path = Path('images/10jul2019_A11.tif')

    >>> date, plot = path.stem.split('_')

    >>> date
    '10jul2019'

    >>> plot
    'A11'

    We'll just go ahead and turn the date into a Pandas Timestamp -- more on Pandas
    later

    >>> import pandas as pd

    >>> date = Timestamp(date)

    >>> date
    Timestamp('2019-07-10 00:00:00')

    Finally, after defining the function:

    >>> proc_img(path)
    (Timestamp('2019-07-10 00:00:00'), 'A11', 0.13098297119140626)
    '''
    # break up file name without extension
    date, plot = path.stem.split('_')
    # pandas is really good at figuring out dates
    date = Timestamp(date)
    # get cover number
    cover = img_to_cc(path)
    # return tuple
    return date, plot, cover

def proc_img_dir(path):
    '''process a directory of tetracam images in a single process


    Parameters
    ----------
    path: str or pathlib.Path


    Returns
    -------
    pandas.DataFrame


    Notes
    -----
    To automate processing, we need to iterate over the directory.

    >>> path = Path('images')

    >>> [p.stem for p in path.iterdir()]
    ['24jul2019_A11', '24jul2019_A12', '10jul2019_A13', '17jul2019_A13',
     '17jul2019_A11', '10jul2019_A12', '17jul2019_A12', '10jul2019_A11',
     '24jul2019_A13']


    That's all of our images. What you just saw is called a list comprehension.
    It's a sort of compressed loop syntax that can be very useful, sometimes
    faster, and always convenient. It's equivalent to:

    >>> tmp = []

    >>> for p in path.iterdir():
    ...     tmp.append(p.stem)

    >>> tmp
    ['24jul2019_A11', '24jul2019_A12', '10jul2019_A13', '17jul2019_A13',
     '17jul2019_A11', '10jul2019_A12', '17jul2019_A12', '10jul2019_A11',
     '24jul2019_A13']

    Let's see what happens when we use proc_img in a list comprehension.

    >>> tmp = [proc_img(p) for p in path.iterdir()]

    >>> tmp
    [(Timestamp('2019-07-24 00:00:00'), 'A11', 0.33957977294921876),
     (Timestamp('2019-07-24 00:00:00'), 'A12', 0.32648239135742185),
     (Timestamp('2019-07-10 00:00:00'), 'A13', 0.081756591796875),
     (Timestamp('2019-07-17 00:00:00'), 'A13', 0.14202880859375),
     (Timestamp('2019-07-17 00:00:00'), 'A11', 0.2568473815917969),
     (Timestamp('2019-07-10 00:00:00'), 'A12', 0.08536148071289062),
     (Timestamp('2019-07-17 00:00:00'), 'A12', 0.18732681274414062),
     (Timestamp('2019-07-10 00:00:00'), 'A11', 0.13098297119140626),
     (Timestamp('2019-07-24 00:00:00'), 'A13', 0.2811866760253906)]


    That looks kind of like a table -- maybe we can pass it to the Pandas DataFrame
    constructor along with some column names

    >>> df = DataFrame(tmp, columns=['date', 'plot', 'cover'])

    >>> df
            date plot     cover
    0 2019-07-24  A11  0.339580
    1 2019-07-24  A12  0.326482
    2 2019-07-10  A13  0.081757
    3 2019-07-17  A13  0.142029
    4 2019-07-17  A11  0.256847
    5 2019-07-10  A12  0.085361
    6 2019-07-17  A12  0.187327
    7 2019-07-10  A11  0.130983
    8 2019-07-24  A13  0.281187


    Setting an index does a few things, but for now it just makes it look nicer

    >>> df = df.set_index(['date', 'plot']).sort_index()

    >>> df
                        cover
    date       plot
    2019-07-10 A11   0.130983
               A12   0.085361
               A13   0.081757
    2019-07-17 A11   0.256847
               A12   0.187327
               A13   0.142029
    2019-07-24 A11   0.339580
               A12   0.326482
               A13   0.281187

    A comprehension wrapped in parentheses is call a generator expression. It's
    like a regular comprehension, except that results are generated on demand.
    Hopefully this allows us to skip some steps, since we aren't passing an
    intermediate object to the DataFrame constructor.

    >>> gen = (n for n in [1,2,3])

    >>> gen
    <generator object <genexpr> at ...>

    >>> next(gen)
    1

    >>> next(gen)
    2

    >>> next(gen)
    3

    >>> next(gen)
    Traceback (most recent call last):
      File ..., in __run
        compileflags, 1), test.globs)
      File "<doctest __main__.proc_img_dir[20]>", line 1, in <module>
        next(gen)
    StopIteration


    We could do something similar with a function, but it's more cumbersome

    >>> def list_gen(input):
    ...     for n in input:
    ...         yield n

    >>> gen = list_gen([1,2,3])

    >>> gen
    <generator object list_gen at ...>

    >>> next(gen)
    1

    Finally:

    >>> proc_img_dir('images')
                           cover
    date       plot
    2019-07-10 A11   0.130983
               A12   0.085361
               A13   0.081757
    2019-07-17 A11   0.256847
               A12   0.187327
               A13   0.142029
    2019-07-24 A11   0.339580
               A12   0.326482
               A13   0.281187
    '''
    # convert to path object
    path = Path(path)
    # as generator
    res = (proc_img(p) for p in path.iterdir())
    # maybe this is better?
    res = DataFrame(res, columns=['date', 'plot', 'cover'])
    # return pretty frame
    return res.set_index(['date', 'plot']).sort_index()

'''
Anyway, What if we have lots of CPUs and we want to go even faster? Let's make
it work in parallel.
'''

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
    # if we leave this as a generator, map isn't really going to work
    imgs = list(Path(path).iterdir())
    # save one for the OS
    cpus = cpu_count() - 1
    if nproc and nproc < cpus: # if limit specified and we're over
        cpus = nproc # drop down to limit
    chunksize = ceil(len(imgs) / cpus) # images per process, round up
    with Pool(cpus) as pool: # set up process pool in context manager
        tmp = pool.map(proc_img, imgs, chunksize) # lazy version
        df = DataFrame(tmp, columns=['date', 'plot', 'cover'])
    return df.set_index(['date', 'plot']).sort_index()

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
    img = Image.merge(mode='RGB',
        bands=(mtif[BANDS.index(b)] for b in (r, g, b)))
    img.show()


'''
finally, do some tests and profiling to show the differences
'''


if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=False, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
