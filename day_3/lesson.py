'''Day 3

    Today, we'll start working with arrays and images.

    First, open Atom. Bring up the lesson from last week -- this will let atom
    know that you want to work in the training repository -- normally you
    would be working on a particular file. In the lower right you should see
    a button that says "fetch." Click it, and it should say "pull." Click it
    again to pull this week's lesson.

    Next, open anaconda prompt and enter the following commands to activate
    the training environment, install the pillow module, navigate to your
    github repository, and start the iPython interpreter:

conda activate trng

conda install pillow scikit-image

cd github/training/day_3

ipython


    Now we'll import Pillow. This package is kind of odd, because it's called
    Pillow, but we import it as PIL. Pillow is a fork of the original PIL
    (Python Imaging Library), which is no longer maintained. The maintainers of
    Pillow have elected to retain PIL as the actual module name. No one should
    ever use PIL, but it's going to look like we are. This is helpful if you're
    trying to maintain compatibility, confusing otherwise. Lots of things about
    Pillow are confusing, so we'll just import the Image module (which looks
    like a class) directly and move on.

>>> from PIL import Image


    Next, we can initialize an Image object from a string filepath by using one
    of the module's factory functions, which looks like a class method, but
    isn't. Read PEP 8 (https://www.python.org/dev/peps/pep-0008/) for more on
    naming conventions, but also note this line:

        "In particular: do not break backwards compatibility just to comply with
        this PEP!"

>>> img = Image.open('images/20190815_A.tif')


    Now we can use the show method to take a look at what we're working with:

>>> img.show()


    We happen to know that these are all six band images, so we are immediately
    suspicious of this greyscale image, but it's nice that there's something.
    Let's look at what bands are available in our image:

>>> img.getbands()
('R', 'G', 'B')


    Hmmm, the plot thickens. Let's inspect the actual values. For this, we'll
    use NumPy:

>>> import numpy as np


    Helpfully, when Pillow Images are passed to NumPy's array constructor, you
    get back what you would expect -- this is no accident, Pillow is actually
    pretty great. The <BLANKLINE>s here are for testing, your output won't
    include them.

>>> np.array(img)
array([[[140, 140, 140],
        [133, 133, 133],
        [136, 136, 136],
        ...,
        [181, 181, 181],
        [176, 176, 176],
        [162, 162, 162]],
<BLANKLINE>
       [[138, 138, 138],
        [133, 133, 133],
        [132, 132, 132],
        ...,
        [191, 191, 191],
        [183, 183, 183],
        [165, 165, 165]],
<BLANKLINE>
       [[143, 143, 143],
        [138, 138, 138],
        [130, 130, 130],
        ...,
        [197, 197, 197],
        [183, 183, 183],
        [168, 168, 168]],
<BLANKLINE>
       ...,
<BLANKLINE>
       [[ 95,  95,  95],
        [ 95,  95,  95],
        [ 96,  96,  96],
        ...,
        [132, 132, 132],
        [134, 134, 134],
        [145, 145, 145]],
<BLANKLINE>
       [[100, 100, 100],
        [ 95,  95,  95],
        [ 97,  97,  97],
        ...,
        [125, 125, 125],
        [130, 130, 130],
        [134, 134, 134]],
<BLANKLINE>
       [[101, 101, 101],
        [ 93,  93,  93],
        [ 99,  99,  99],
        ...,
        [120, 120, 120],
        [135, 135, 135],
        [131, 131, 131]]], dtype=uint8)


    Let's unpack this -- it's not unlike our maze from last week, but it's
    quite a bit bigger. How big?

>>> a = np.array(img)

>>> a.shape
(1024, 1280, 3)


    Recall that an array like this is an array of rows, where each element is
    a pixel. So, we can see that our image is 1024 pixels tall, 1280 pixels
    wide, with three bands. The ellipses in the output represent either a
    continuation of one row, or a continuation of the rows, depending on
    indentation level. If you look closely at the brackets and commas, this will
    make sense. Neat!

    It looks like we have a greyscale RGB image, since we know it's black and
    white, and each pixel has three identical values. This might be fine for
    representing a black and white image on the internet or something, but it's
    pretty redundant for our purposes. Let's just get the first from each pixel

>>> a = np.array(img.getchannel(0))

>>> a
array([[140, 133, 136, ..., 181, 176, 162],
       [138, 133, 132, ..., 191, 183, 165],
       [143, 138, 130, ..., 197, 183, 168],
       ...,
       [ 95,  95,  96, ..., 132, 134, 145],
       [100,  95,  97, ..., 125, 130, 134],
       [101,  93,  99, ..., 120, 135, 131]], dtype=uint8)


    What about this "dtype=uint8?" dtype is short for data type. uint is
    short for "unsigned integer." To understand what unsigned means, we need
    to know what an 8 bit integer is. In computer hardware, a byte (8 bits)
    is the smallest addressable unit of memory. A byte is literally a series
    of 8 little switchs all in a row, and each one can either be on or off. 8
    bits all set to on/True/1 make 255. This is binary.

>>> 0b11111111
255


    8 off/false/0 bits make... 0.

>>> 0b00000000
0


    That gives us a total of 256 possible values. What about the unsigned part?
    A signed integer just splits the values in half, and uses the first bit as
    a +/- sign, where 1 indicates a negative value. Thus, these 8-bit integers
    range from -128 to 127, since negative 0 makes no sense. Critically, we
    still have 256 possible values, we just interpret them differently.

>>> 0b01111111
127


    Let's see what happens if we tell Numpy that our integers are actually
    signed:

>>> a.astype(np.int8)
array([[-116, -123, -120, ...,  -75,  -80,  -94],
       [-118, -123, -124, ...,  -65,  -73,  -91],
       [-113, -118, -126, ...,  -59,  -73,  -88],
       ...,
       [  95,   95,   96, ..., -124, -122, -111],
       [ 100,   95,   97, ...,  125, -126, -122],
       [ 101,   93,   99, ...,  120, -121, -125]], dtype=int8)


    Funky -- everything that was less than 128 stayed the same, while everything
    bigger got negative and different. If we want to represent signed integers
    this big, we need to use two bytes.

>>> a.astype(np.int16)
    array([[140, 133, 136, ..., 181, 176, 162],
           [138, 133, 132, ..., 191, 183, 165],
           [143, 138, 130, ..., 197, 183, 168],
           ...,
           [ 95,  95,  96, ..., 132, 134, 145],
           [100,  95,  97, ..., 125, 130, 134],
           [101,  93,  99, ..., 120, 135, 131]], dtype=int16)


    Great! Unfortunately, this is pretty silly, since we don't have any negative
    numbers and using the bigger integers doubles the size of our array.

>>> a.astype(np.int16).nbytes
2621440

>>> a.nbytes
1310720


    Since we know each value in our array should be one byte, we should be
    able to arrive at this number indepedently.

>>> a.nbytes == 1024 * 1280
True


    Great! Now that that's out of the way, you might be wondering if the images
    are really stored as three identical bands for each band, since it would
    make each one three times bigger than it needs to be. Let's dig deeper. We
    have six bands, so if each one is duplicated three times, the size of our
    images should be something like:

>>> a.nbytes * 6 * 3 / 1000000
23.59296

>>> import os

>>> os.path.getsize('images/20190815_A.tif') / 1000000
23.596264


    Uh-oh.

    Anyway, what happened to our other five bands? Well, it turns out
    that each image is actually a series of six images in a format called a
    multi-page tiff, presumably to make it easier to browse them with simple
    tools. Our original image object was just grabbing the first band.
    Fortunately, Pillow has us covered.

>>> from PIL import ImageSequence

>>> mtif = ImageSequence.Iterator(img)

>>> np.array(mtif[0].getchannel(0))
array([[140, 133, 136, ..., 181, 176, 162],
       [138, 133, 132, ..., 191, 183, 165],
       [143, 138, 130, ..., 197, 183, 168],
       ...,
       [ 95,  95,  96, ..., 132, 134, 145],
       [100,  95,  97, ..., 125, 130, 134],
       [101,  93,  99, ..., 120, 135, 131]], dtype=uint8)

>>> np.array(mtif[5].getchannel(0))
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       ...,
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0]], dtype=uint8)


    It looks like we found them, but which band is which? Thanks to Kevin, we
    know that the band order is as follows:

>>> BANDS = ('nir', 'blue', 'green', 'yellow', 'red', 'edge')


    If we want to know the index of a particular band (its number), we can
    use the index method of BANDS

>>> BANDS.index('red')
4

>>> BANDS.index('nir')
0


    Now we can make a little function to help us get bands

>>> def get_band(mtif, name):
...     return mtif[BANDS.index(name)].getchannel(0)


    If we want to reassemble a color image, it's not too tough

>>> rgb = Image.merge(
...     mode='RGB',
...     bands=(
...         get_band(mtif, 'red'),
...         get_band(mtif, 'green'),
...         get_band(mtif, 'blue')))

>>> rgb.show()


    Let's make that a function too

>>> def show_rgb(mtif, r='red', g='green', b='blue'):
...     img = Image.merge(
...         mode='RGB',
...         bands=(
...             get_band(mtif, r),
...             get_band(mtif, g),
...             get_band(mtif, b)))
...     img.show()


    We'll use it to get a false color image

>>> show_rgb(mtif, 'nir', 'red', 'green')


    Let's get out the bands we need for NDVI as arrays.

>>> red = np.array(get_band(mtif, 'red'))

>>> nir = np.array(get_band(mtif, 'nir'))


    Now we need to revisit arrays. Remember how we said that low level array
    operations are fast? Why? Since we know the size of each piece of
    information, and each is physically lined up, it's easy for the processor
    to just run over the whole array by incrementing the address by the size
    of each element, and believing you about what it is (we've seen how this
    can go wrong). Numpy does this automatically.

>>> from timeit import timeit

>>> good = timeit('red * red', number=10, globals=globals())


    Alternatively, we can convert the array to a list and "manually" loop over
    the rows and columns. The result is the same, but the the approach is
    vastly different. Remember that a list is a collection of references to
    other things that could be anything.

>>> bad_res = np.zeros_like(red).tolist()

>>> bad_red = red.tolist()

>>> bad = timeit("""
... for i, row in enumerate(bad_red):
...         for j, val in enumerate(row):
...             bad_res[i][j] = val * val
... """, number=10, globals=globals())

>>> round(bad / good)
800


    This isn't the most scientific test, but hopefully you get the point. This
    is a very simple operation. With more complex operations, the "bad" option
    becomes prohibitively slow.

    Let's create a function for NDVI

>>> def ndvi(nir, red):
...     return (nir - red) / (nir + red)

>>> res = ndvi(nir, red).round(2)

>>> res
array([[1.  , 1.  , 1.  , ..., 1.  , 1.  , 1.  ],
       [1.  , 1.  , 1.  , ..., 1.  , 1.  , 1.  ],
       [1.  , 1.  , 1.  , ..., 1.  , 1.  , 1.  ],
       ...,
       [0.96, 0.94, d0.96, ..., 0.97, 1.  , 1.  ],
       [0.94, 0.92, 0.94, ..., 0.97, 1.  , 1.  ],
       [0.96, 0.94, 0.94, ..., 0.92, 1.  , 1.  ]])

>>> Image.fromarray(res * 255).show()


    Whoa -- what's with all the holes? Let's see what happens if we subtract a
    an unsigned integer from another, smaller unsigned integer.

>>> np.array([1, 2, 3], np.uint8) - np.array([4, 5, 6], np.uint8)
array([253, 253, 253], dtype=uint8)


    The exact reason for this is deeper magic than I understand, but it's
    clearly not right, and has to do with the fact that the result of the
    operation cannot be represented by an unsigned 8 bit integer. This can
    happen frequently in the numerator.

    Similarly, lets see what happens when the denominator is larger than 255.

>>> np.array([200], np.uint8) + np.array([200], np.uint8)
array([144], dtype=uint8)


    More deep magic. The broomsticks are running wild. Let's see what what the
    range of values in res is.

>>> res.min(); res.max()
0.01
inf


    inf is short for infinity, and is the result of division by zero. Obviously
    addition of two positive numbers should never produce 0. The results of
    these out-of-range operations are highly unpredictable. Let's redefine our
    function to convert both bands to a 16-bit signed integer, which has a
    range of –32768 to 32767.


>>> def ndvi(nir, red):
...     red, nir = red.astype(np.int16), nir.astype(np.int16)
...     return (nir - red) / (nir + red)

>>> res = ndvi(nir, red)

>>> Image.fromarray(res * 255).show()

>>> res.min(); res.max()
-0.06276150627615062
1.0


    Wonderful! Now we can use Otsu's method to get a threshold value that will
    divide this image into two categories -- our assumption is that the two main
    categories will always be plant and not plant, but this may not be true at
    the beginning and end of the season.

>>> from skimage.filters import threshold_otsu

>>> th = threshold_otsu(res[np.isfinite(res)])

>>> th
0.8235649843096234


    That's pretty neat, but we probably need to talk about what just happened.
    First up is np.isfinite. nan is used to represent missing or nonsense data,
    and the result of any operation with nan is nan -- this is useful to avoid
    propagating nonsense. We've already talked about inf. isfinite returns true
    for any value except those two.

>>> np.nan * 10
nan

>>> np.inf - 5
inf

>>> mask = np.isfinite(np.array([1, 0, np.nan, np.inf]))

>>> mask
array([ True,  True, False, False])


    Indexing an array with another array returns only those values where the
    indexer is True (assuming both arrays have the same shape)

>>> tmp = np.array([1, 2, 3, 4])

>>> tmp[mask]
array([1, 2])


    Technically, we could still have a zero in the denominator if red and nir
    are both zero. This shouldn't happen, but can if exposures are wonky. In
    that case, we're really just looking at darkness and shouldn't include it
    in our threshold calculation because it could be anything. We definitely
    don't want to include nan, so we exclude both nan and inf from the
    calculation.

    Now we can change values above the threshold to 1 (True/plant) and values
    below the threshold to 0 (false/not-plant) with another set of indexers.
    The where function says: where arg 0 is True, make the value arg 1; where
    arg 0 is False, make the value arg 2.

>>> cls = np.where(res > th, 1, 0).astype(np.uint8)

    Let's see what that looks like with tmp


>>> tmp > 2
array([False, False,  True,  True])

>>> np.where(tmp > 2, 1, 0)
array([0, 0, 1, 1])


    Let's take a look at the classified image and compare to the RGB.

>>> Image.fromarray(cls * 255).show()

>>> show_rgb(mtif)


    Seems reasonably convincing, but we still want to knock this down to a plain
    canopy cover percentage. To do that, we again exclude nan and inf.

>>> fin = cls[np.isfinite(res)]


    Since every pixel in fin is now either 1 or zero, summing the image gives
    us the number of plant pixels. If we divide that by the total number of
    pixels, we have fractional canopy cover

>>> (fin.sum() / fin.size).round(5)
0.74309

'''


if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=True, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
