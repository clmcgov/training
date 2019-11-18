'''
Before we get into the applied part of today's lesson, I want to touch on some
concepts in programming. I'm not really expecting you to retain any of this,
but I do want to give you some context for the things that I do want you to
retain.

If you're used to writing scripts in R and Python and then "running" those
scripts on a dataset, then you're used to imperative programming:

>>> res = []

# sprinkler
>>> eff = 75

>>> i_gross = 30

>>> def i_net():
...     return i_gross * eff / 100

>>> res.append(i_net())

#drip
>>> eff = 90

>>> res.append(i_net())

>>> res
[22.5, 27.0]

This style is called imperative programming because you're mostly concerned with
telling the computer how to change the state of the program and what to do with
that state in a sequence of instructions producing some final result. Programs
like this are usually intended to "run" once, and can be thought of as a sort of
check-list. The outcome of any operation is usually dependent on the value of
some state variable, such that the same function called with the same arguments
may return different results.

This becomes problematic as the program grows, because it becomes difficult to
understand the way the state is changing, or what it actually should be at any
given time (Anyone ever tried to untangle 100000 lines of fortran?).

This is not to say that this style is wrong -- fundamentally, this is how
computers work. All programming is imperative programming once it gets down to
machine code. Unfortunately, this isn't great for humans who might want to
modify the program or explain it to their friends.

    NOTE: Constants and state (global) variables are not the same thing. They
    may be declared in the same place, but constants do not vary and variables
    are inconstant. Recall that there are no true constants in Python, only
    globals written in all caps. Only you can prevent global variables.

Enter functional programming.

The idea behind functional programming is that there should be no state -- the
return value of any function should depend entirely on the arguments passed.
This makes for code that is easier to understand, and also more modular.
Additionally, these are functions in the mathematical sense, which opens up a
whole world of thought and knowledge.
'''

def check_eff(eff):
    '''
    This function always returns nothing unless it raises an error, in
    which case execution stops and its return value is not relevant.
    '''
    if not 100 >= eff >= 0:
        raise ValueError('eff must be between 0 and 100')

def i_net(i_gross, eff):
    '''
    This is better. Now it's easy to swap out components (maybe we want to restrict
    eff to a narrower range), and also to reuse them (maybe we want this to be
    part of an irrigation scheduler).

    >>> i_net(30, 75)
    22.5

    >>> i_net(30, 90)
    27.0
    '''
    check_eff(eff)
    return i_gross * eff / 100

'''
Suppose we want to hide some of this from a user and create an object that
just represents net irrigation
'''

class INet:
    '''
    This is a class -- a little callable object that remembers irrigation
    efficiency and makes sure it conforms to some reasonable value. We can
    represent a couple of systems in a more idiomatic fashion. It's basically
    just the imperative version in a cage with an extra check -- it helps us
    manage state, it doesn't eliminate it.

    >>> sprinkler = INet(75)

    >>> drip = INet(90)

    >>> sprinkler(30)
    22.5

    >>> drip(30)
    27.0

    >>> drip.eff = 95

    >>> drip(30)
    28.5
    '''

    def __init__(self, eff):
        self.eff = eff

    def __call__(self, i_gross):
        return i_gross * self.eff / 100

    @property
    def eff(self):
        return self._eff

    @eff.setter
    def eff(self, val):
        if not 100 >= val >= 0:
            raise ValueError('eff must be between 0 and 100')
        self._eff = val

'''
These implementations are all identical in the ways that count, they just take
different approaches to scoping. Scoping is the idea of keeping variables in
little fenced areas, like a data zoo.

In the imperative version, our variables are just running wild in the global
scope -- this can get ugly quickly.

In the functional version, we contained our variables in the scopes of the
functions -- they only exist inside the functions. We can have lots of
functions doing lots of things to the "same" variable, but in reality, each is
doing it to its own little version, and then passing the result to another.
This makes it easy to know exactly what's going on at all times.

The object oriented approach gives each instance of the object its own little
namespace -- "self." This doesn't really solve the problems of state, but it
does mean that we can have lots of states running around at the same time.
Whether or not that's a good thing depends on our design.
'''

def closure_func(eff):
    '''
    Just for fun, we can get a similar result using a closure (a functional
    approach). Here we have enclosed the variable in the function. This function
    will return the same result when called with the same argument every time,
    and that result will return the same result every time.

    >>> sprinkler = closure_func(75)

    >>> drip = closure_func(90)

    >>> sprinkler(30)
    22.5

    >>> drip(30)
    27.0
    '''
    check_eff(eff)
    def i_net(i_gross):
        return i_gross * eff / 100
    return i_net

def system_factory(eff):
    '''
    Really, objects are just dictionaries full of values and functions. The
    functions (methods) are closures with a reference to the dictionary that
    contains them (self). We can replicate the object-oriented verison without
    any special syntax using a factory function.

    >>> sys = system_factory(75)

    >>> sys['i_net'](30)
    22.5

    >>> sys['eff'] = 90

    >>> sys['i_net'](30)
    27.0
    '''
    d = {'eff': eff}
    def i_net(i_gross):
        return i_gross * d['eff'] / 100
    d['i_net'] = i_net
    return d

class System:
    '''
    The main advantage of objects is abstraction -- we can use them to define an
    interface that hides some of the complexity of a program from the user,
    allowing them to focus on the parts that are important to them, rather than
    your implementation. Python offers lots of nice little hooks to help you do
    cool things -- these are called "magic methods," and they all start and end
    with double underscores.

    >>> mysys = System('sprinkler')

    >>> mysys
    Sprinkler System (75% efficient)

    >>> mysys(30)
    22.5

    >>> mysys.type = 'drip'

    >>> mysys
    Drip System (90% efficient)

    >>> mysys(30)
    27.0
    '''

    TYPES = {
        'sprinkler': 75,
        'drip': 90,
        'flood': 50}

    def __init__(self, type):
        self.type = type

    def __call__(self, i_gross):
        return i_gross * self.eff / 100

    def __repr__(self):
        # this is not a good use of __repr__, just an example
        res =  '{} System ({}% efficient)'
        return res.format(self.type.title(), self.eff)

    @property
    def eff(self):
        return self._eff

    @property
    def type(self):
        tmp = {v: k for k, v in self.TYPES.items()}
        return tmp[self._eff]

    @type.setter
    def type(self, val):
        self._eff = self.TYPES[val.lower()]

'''
Now the user doesn't need to know anything about the implementation. On the
other hand, we've now got a bunch of garbage sitting on top of essentially the
same implementation. If the garbage helps people use our software by hiding
things they shouldn't have to know, then it's not garbage. If the garbage hides
things the user really should be aware of, then it's worse than garbage. If the
problem is simple, then we've probably made some kind of Rube Goldberg garbage
sculpture.

By now it should be easy to see that there are many ways to approach a problem.
It should also be clear that objects can be quite powerful (everything in Python
is actually an object). On the other hand, I hope you can see that objects in no
way address the root problems of imperative programming, they just make it
easier to avoid the consequences. OOP is not magic.

Objects should be seen as a way of creating interfaces. I do not reccomend them
as ways of thinking about problems for the same reason that I wouldn't recommend
imperative programming. On the other hand, if you try to hand someone else 10000
lines of functions addressing a complex problem, it may take them a while to get
started. Ideally, an object will be a clear, simple interface to a functional
workflow.

This concludes the programming discussion -- time to get back to image
processing.

Let's wrap the whole analysis into a set of functions. We'll use composition to
work up to a top level function. The following two functions just summarize last
week's work. See comments and/or the previous lesson for more infomration
'''
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
    img = Image.open(path)
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
        tmp = pool.imap_unordered(proc_img, imgs, chunksize) # lazy version
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
