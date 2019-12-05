'''

>>> from cover import *

Today we'll wrap our image processing protocol into a set of functions, and
use those functions to process a directory of files in parallel. Additionally,
we'll take random samples of each image.


We need to parse the filenames, so we'll first get the stem of the path object
-- the filename with no extension. We can use the string split method with
multiple assignment to extract the information.

>>> from pathlib import Path

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

>>> parse_name(path)
(Timestamp('2019-07-10 00:00:00'), 'A11')

Now we can use parse_name in a function to process individual images.


After extracting the timestamp and plot, we open the image using a context
manager (line 64). Whenever a file is opened, it must also be closed. A context
manager in a with/as statement defines some clean-up action that should be taken
after the indented block executes -- closing the file in this case.

Within the context manager, we extract the band of interest as before. We
calculate NDVI over the whole image, since each pixel is independent in that
calculation.

Next we subsample the image, obtaining 10 random samples, each a square
representing 10% of the image. Let's take some time to dive into the sample
function.

First, we get the dimensions of the image:

>>> y, x = 1024, 1280


Then, we can get 10% of the overall area of the image in pixels:

>>> 0.1 * y * x
131072.0


Next, we take the square-root of of that area to find the length of one side
of a square with that area, and round down to the nearest integer.

>>> int(sqrt(0.1 * y * x))
362


The arange(n) function produces an array of consecutive integers from 0 to n.

>>> from numpy import arange, array, random

>>> arange(362)
array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
        13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,
        26,  27,  28,  29,  30,  31,  32,  33,  34,  35,  36,  37,  38,
        39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,
        52,  53,  54,  55,  56,  57,  58,  59,  60,  61,  62,  63,  64,
        65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,
        78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,
        91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102, 103,
       104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
       117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129,
       130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
       143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155,
       156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
       169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181,
       182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194,
       195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207,
       208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
       221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233,
       234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246,
       247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259,
       260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272,
       273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285,
       286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298,
       299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311,
       312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324,
       325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337,
       338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350,
       351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361])


The next lines are a little bit magical. You probably recognize the __getitem__
syntax in arange(s)[None, :], but not much else. The colon (:) is a shortcut to
Python's slice object, much as quotes are a shortcut to the string object. A
slice represents a span such that 1:7 means everything between one and 7.

>>> help(slice)
Help on class slice in module builtins:
<BLANKLINE>
class slice(object)
 |  slice(stop)
 |  slice(start, stop[, step])
 |
 |  Create a slice object.  This is used for extended slicing (e.g. a[0:10:2]).
 |
 |  Methods defined here:
 |
 |  __eq__(self, value, /)
 |      Return self==value.
 |
 |  __ge__(self, value, /)
 |      Return self>=value.
 |
 |  __getattribute__(self, name, /)
 |      Return getattr(self, name).
 |
 |  __gt__(self, value, /)
 |      Return self>value.
 |
 |  __le__(self, value, /)
 |      Return self<=value.
 |
 |  __lt__(self, value, /)
 |      Return self<value.
 |
 |  __ne__(self, value, /)
 |      Return self!=value.
 |
 |  __reduce__(...)
 |      Return state information for pickling.
 |
 |  __repr__(self, /)
 |      Return repr(self).
 |
 |  indices(...)
 |      S.indices(len) -> (start, stop, stride)
 |
 |      Assuming a sequence of length len, calculate the start and stop
 |      indices, and the stride length of the extended slice described by
 |      S. Out of bounds indices are clipped in a manner consistent with the
 |      handling of normal slices.
 |
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |
 |  __new__(*args, **kwargs) from builtins.type
 |      Create and return a new object.  See help(type) for accurate signature.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  start
 |
 |  step
 |
 |  stop
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __hash__ = None
<BLANKLINE>


>>> l = [1, 2, 3, 4, 5]


>>> l[2:4]
[3, 4]

>>> l[slice(2, 4)]
[3, 4]


>>> l[2:]
[3, 4, 5]

>>> l[slice(2, None)]
[3, 4, 5]


>>> l[:4]
[1, 2, 3, 4]

>>> l[slice(None, 4)]
[1, 2, 3, 4]


>>> l[:]
[1, 2, 3, 4, 5]

>>> l[slice(None, None)]
[1, 2, 3, 4, 5]


This is way of indexing works on numpy arrays too, but in multiple dimensions.
This is simlar to the way we indexed nested lists, but slightly different
because a numpy array is not a nested data structure, but a single n-dimensional
array.

>>> l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

>>> l
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]


>>> a = array(l)

>>> a
array([[1, 2, 3],
       [4, 5, 6],
       [7, 8, 9]])


>>> l[1][2]
6

>>> a[1, 2]
6

>>> l[1][:2]
[4, 5]

>>> a[1, :2]
array([4, 5])

Here's where things get really different:

>>> a[1:, 2]
array([6, 9])

>>> l[1:][2]
Traceback (most recent call last):
  File ..., line 1329, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__[34]>", line 1, in <module>
    l[1:][2]
IndexError: list index out of range

This is just one more way to get around a numpy array. Recall that we've
already seen how we can use a same-shape indexer:

>>> idxr = array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool)

>>> idxr
array([[False,  True, False],
       [ True, False,  True],
       [False,  True, False]])

>>> a[idxr]
array([2, 4, 6, 8])


getting  back to the problem at hand, what about arange(s)[None, :]? Well, now
we know that this evaluates to arange(s)[None, slice(None, None)], but what
about the plain old None? ndarray's __getitem__ method is defined such that
None as an indexer means "add an extra dimension."

>>> a = arange(6)

>>> a
array([0, 1, 2, 3, 4, 5])

>>> a.shape
(6,)

six elements


>>> a[:, None]
array([[0],
       [1],
       [2],
       [3],
       [4],
       [5]])

>>> a[:, None].shape
(6, 1)

six rows, one column


>>> a[None, :]
array([[0, 1, 2, 3, 4, 5]])

>>> a[None, :].shape
(1, 6)

one row, six columns


This is a little magical -- trial and error goes a long way. Great, but what
happens when we add them?

>>> idxr = a[None, :] + a[:, None]

>>> idxr
array([[ 0,  1,  2,  3,  4,  5],
       [ 1,  2,  3,  4,  5,  6],
       [ 2,  3,  4,  5,  6,  7],
       [ 3,  4,  5,  6,  7,  8],
       [ 4,  5,  6,  7,  8,  9],
       [ 5,  6,  7,  8,  9, 10]])

This is called "broadcasting." Again, it's a little magical, but if you look
closely at the addition terms (above) and the result, it makes some sense.

Let's see what happens when we apply this indexer to a one-dimensional array:

>>> b = array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'])

>>> b[idxr]
array([['a', 'b', 'c', 'd', 'e', 'f'],
       ['b', 'c', 'd', 'e', 'f', 'g'],
       ['c', 'd', 'e', 'f', 'g', 'h'],
       ['d', 'e', 'f', 'g', 'h', 'i'],
       ['e', 'f', 'g', 'h', 'i', 'j'],
       ['f', 'g', 'h', 'i', 'j', 'k']], dtype='<U1')

Whoa, what? This is yet another way of indexing a numpy array. We said: "give
me an array like the indexer I passed, but at each poisition, give me the
element from b at the specified index.

So what if we want the indexes to be steadily increasing? That's where the
multiplication term comes in:

>>> 6 * a[:, None]
array([[ 0],
       [ 5],
       [10],
       [15],
       [20],
       [25]])

>>> a[None, :] + 6 * a[:, None]
array([[ 0,  1,  2,  3,  4,  5],
       [ 6,  7,  8,  9, 10, 11],
       [12, 13, 14, 15, 16, 17],
       [18, 19, 20, 21, 22, 23],
       [24, 25, 26, 27, 28, 29],
       [30, 31, 32, 33, 34, 35]])

Neato! Let's use this technique to make a 100 x 100 "image"

>>> img = arange(100)[None, :] + 100 * arange(100)[:, None]

>>> img
array([[   0,    1,    2, ...,   97,   98,   99],
       [ 100,  101,  102, ...,  197,  198,  199],
       [ 200,  201,  202, ...,  297,  298,  299],
       ...,
       [9700, 9701, 9702, ..., 9797, 9798, 9799],
       [9800, 9801, 9802, ..., 9897, 9898, 9899],
       [9900, 9901, 9902, ..., 9997, 9998, 9999]])

This "image" just contains the 1-D index of each pixel at each pixel. Now we're
going to flatten it:

>>> img.flatten()
array([   0,    1,    2, ..., 9997, 9998, 9999])

Could we have just said arange(10000)? Yes, but we're trying to learn.

So now let's make an indexer that will grab a 5x5 square from our image:

>>> idxr = arange(5)[None, :] + 100 * arange(5)[:, None]

>>> idxr
array([[  0,   1,   2,   3,   4],
       [100, 101, 102, 103, 104],
       [200, 201, 202, 203, 204],
       [300, 301, 302, 303, 304],
       [400, 401, 402, 403, 404]])

Keeping in mind that our "image" is 100 X 100, we can see that this is the
upper left corner of it. Let's see what happens when we apply our indexer to the
flattened array:

>>> img.flatten()[idxr]
array([[  0,   1,   2,   3,   4],
       [100, 101, 102, 103, 104],
       [200, 201, 202, 203, 204],
       [300, 301, 302, 303, 304],
       [400, 401, 402, 403, 404]])

It helpfully rebuilt our indexer. But what if we add an integer to the indexer?

>>> idxr + 500
array([[500, 501, 502, 503, 504],
       [600, 601, 602, 603, 604],
       [700, 701, 702, 703, 704],
       [800, 801, 802, 803, 804],
       [900, 901, 902, 903, 904]])

>>> img.flatten()[idxr + 500]
array([[500, 501, 502, 503, 504],
       [600, 601, 602, 603, 604],
       [700, 701, 702, 703, 704],
       [800, 801, 802, 803, 804],
       [900, 901, 902, 903, 904]])

Same thing, except now the upper left corner is at index 500 in the flattened
image.

So, if we want a random sample of our image, we can just add a random integer
to our indxer.

BUT WAIT: What if we get a random number like 97 (remember each row has 100
elements)?

>>> img.flatten()[idxr + 97]
array([[ 97,  98,  99, 100, 101],
       [197, 198, 199, 200, 201],
       [297, 298, 299, 300, 301],
       [397, 398, 399, 400, 401],
       [497, 498, 499, 500, 501]])

Recall that the upper right corner of the image was at index 99 -- This sample
is all wonky because the rows of our indexer ran across rows of the image. If we
go too far down the image, the indexes of our indexer will be out of range. How
can we handle this?

>>> idxs = random.randint(0, (100 - 5), 10)

We said: "give me ten random numbers from 0 to 94 (inclusive left, exclusive
right). This way, we always have room for our indexer. This is basically a
random column.

>>> idxs
array([44, 85, 44,  0,  5, 77, 70, 94, 31,  9])

Now we're taking samples from the top of the image (these indices are all in
top row), but we've avoided overflow. We can do somehting very similar to what
we did to construct the indexer and add an integer representing the start of
a random row:

>>> idxs = random.randint(0, 95, 10) + 100 * random.randint(0, 95, 10)

>>> idxs
array([ 948, 8746, 3938, 5937, 7940, 1706, 7252, 3362, 6228, 7026])

Great! Now we have ten random upper left corner indices that won't cause our
window to run past the bottom of the image or wrap around the sides.

Let's get ten random samples:

>>> img = img.flatten()

>>> array([img[idxr + idx] for idx in idxs])
array([[[2031, 2032, 2033, 2034, 2035],
        [2131, 2132, 2133, 2134, 2135],
        [2231, 2232, 2233, 2234, 2235],
        [2331, 2332, 2333, 2334, 2335],
        [2431, 2432, 2433, 2434, 2435]],
<BLANKLINE>
       [[8846, 8847, 8848, 8849, 8850],
        [8946, 8947, 8948, 8949, 8950],
        [9046, 9047, 9048, 9049, 9050],
        [9146, 9147, 9148, 9149, 9150],
        [9246, 9247, 9248, 9249, 9250]],
<BLANKLINE>
       [[1755, 1756, 1757, 1758, 1759],
        [1855, 1856, 1857, 1858, 1859],
        [1955, 1956, 1957, 1958, 1959],
        [2055, 2056, 2057, 2058, 2059],
        [2155, 2156, 2157, 2158, 2159]],
<BLANKLINE>
       [[7889, 7890, 7891, 7892, 7893],
        [7989, 7990, 7991, 7992, 7993],
        [8089, 8090, 8091, 8092, 8093],
        [8189, 8190, 8191, 8192, 8193],
        [8289, 8290, 8291, 8292, 8293]],
<BLANKLINE>
       [[3310, 3311, 3312, 3313, 3314],
        [3410, 3411, 3412, 3413, 3414],
        [3510, 3511, 3512, 3513, 3514],
        [3610, 3611, 3612, 3613, 3614],
        [3710, 3711, 3712, 3713, 3714]],
<BLANKLINE>
       [[1431, 1432, 1433, 1434, 1435],
        [1531, 1532, 1533, 1534, 1535],
        [1631, 1632, 1633, 1634, 1635],
        [1731, 1732, 1733, 1734, 1735],
        [1831, 1832, 1833, 1834, 1835]],
<BLANKLINE>
       [[1406, 1407, 1408, 1409, 1410],
        [1506, 1507, 1508, 1509, 1510],
        [1606, 1607, 1608, 1609, 1610],
        [1706, 1707, 1708, 1709, 1710],
        [1806, 1807, 1808, 1809, 1810]],
<BLANKLINE>
       [[1308, 1309, 1310, 1311, 1312],
        [1408, 1409, 1410, 1411, 1412],
        [1508, 1509, 1510, 1511, 1512],
        [1608, 1609, 1610, 1611, 1612],
        [1708, 1709, 1710, 1711, 1712]],
<BLANKLINE>
       [[3827, 3828, 3829, 3830, 3831],
        [3927, 3928, 3929, 3930, 3931],
        [4027, 4028, 4029, 4030, 4031],
        [4127, 4128, 4129, 4130, 4131],
        [4227, 4228, 4229, 4230, 4231]],
<BLANKLINE>
       [[1632, 1633, 1634, 1635, 1636],
        [1732, 1733, 1734, 1735, 1736],
        [1832, 1833, 1834, 1835, 1836],
        [1932, 1933, 1934, 1935, 1936],
        [2032, 2033, 2034, 2035, 2036]]])


Remember that the last bit was a list comprehension equivalent to:

>>> res = []

>>> for idx in idxs:
...     res.append(img[idxr + idx])

>>> array(res)
array([[[5468, 5469, 5470, 5471, 5472],
        [5568, 5569, 5570, 5571, 5572],
        [5668, 5669, 5670, 5671, 5672],
        [5768, 5769, 5770, 5771, 5772],
        [5868, 5869, 5870, 5871, 5872]],
<BLANKLINE>
       [[6993, 6994, 6995, 6996, 6997],
        [7093, 7094, 7095, 7096, 7097],
        [7193, 7194, 7195, 7196, 7197],
        [7293, 7294, 7295, 7296, 7297],
        [7393, 7394, 7395, 7396, 7397]],
<BLANKLINE>
       [[7127, 7128, 7129, 7130, 7131],
        [7227, 7228, 7229, 7230, 7231],
        [7327, 7328, 7329, 7330, 7331],
        [7427, 7428, 7429, 7430, 7431],
        [7527, 7528, 7529, 7530, 7531]],
<BLANKLINE>
       [[1329, 1330, 1331, 1332, 1333],
        [1429, 1430, 1431, 1432, 1433],
        [1529, 1530, 1531, 1532, 1533],
        [1629, 1630, 1631, 1632, 1633],
        [1729, 1730, 1731, 1732, 1733]],
<BLANKLINE>
       [[1627, 1628, 1629, 1630, 1631],
        [1727, 1728, 1729, 1730, 1731],
        [1827, 1828, 1829, 1830, 1831],
        [1927, 1928, 1929, 1930, 1931],
        [2027, 2028, 2029, 2030, 2031]],
<BLANKLINE>
       [[1702, 1703, 1704, 1705, 1706],
        [1802, 1803, 1804, 1805, 1806],
        [1902, 1903, 1904, 1905, 1906],
        [2002, 2003, 2004, 2005, 2006],
        [2102, 2103, 2104, 2105, 2106]],
<BLANKLINE>
       [[4994, 4995, 4996, 4997, 4998],
        [5094, 5095, 5096, 5097, 5098],
        [5194, 5195, 5196, 5197, 5198],
        [5294, 5295, 5296, 5297, 5298],
        [5394, 5395, 5396, 5397, 5398]],
<BLANKLINE>
       [[1741, 1742, 1743, 1744, 1745],
        [1841, 1842, 1843, 1844, 1845],
        [1941, 1942, 1943, 1944, 1945],
        [2041, 2042, 2043, 2044, 2045],
        [2141, 2142, 2143, 2144, 2145]],
<BLANKLINE>
       [[4165, 4166, 4167, 4168, 4169],
        [4265, 4266, 4267, 4268, 4269],
        [4365, 4366, 4367, 4368, 4369],
        [4465, 4466, 4467, 4468, 4469],
        [4565, 4566, 4567, 4568, 4569]],
<BLANKLINE>
       [[6791, 6792, 6793, 6794, 6795],
        [6891, 6892, 6893, 6894, 6895],
        [6991, 6992, 6993, 6994, 6995],
        [7091, 7092, 7093, 7094, 7095],
        [7191, 7192, 7193, 7194, 7195]]])


This is exactly what the sample function does, but it takes ten samples of 10%
of any reasonable rectangular array.

To prove it, we'll write some code to display samples from an image:

from PIL import Image, ImageSequence

>>> with Image.open('images/10jul2019_A11.tif') as img:
...     nir = array(ImageSequence.Iterator(img)[BANDS.index('nir')])

>>> nir
array([[ 47,  42,  46, ...,  67,  72,  75],
       [ 44,  44,  46, ...,  64,  70,  74],
       [ 47,  52,  53, ...,  61,  66,  70],
       ...,
       [ 42,  42,  51, ..., 106, 109, 114],
       [ 40,  37,  42, ..., 109, 115, 117],
       [ 40,  37,  42, ..., 107, 117, 116]], dtype=uint8)

>>> for a in sample(nir):
...     Image.fromarray(a).show()


Finally, let's get back to the proc_img function. We've already calculated NDVI
(fake) for the whole image, now we just apply our Otsu cover function to each
so that we get a list of ten fractional covers instead of images. We simply
pass that list into the pandas DataFrame constuctor, along with the information
that we extracted from the file name and a rep number:

>>> proc_img('images/10jul2019_A11.tif')
                           cc
date       plot rep
2019-07-10 A11  0    0.106758
                1    0.129613
                2    0.159664
                3    0.161854
                4    0.152979
                5    0.140663
                6    0.145089
                7    0.117548
                8    0.134939
                9    0.198254


Whew! Now let's do a whole directory. For this, we'll use the iterdir method of
the Path object.

>>> path = Path('images')

>>> imgs = tuple(path.iterdir())

>>> imgs
(PosixPath('images/24jul2019_A11.tif'),
 PosixPath('images/24jul2019_A12.tif'),
 PosixPath('images/10jul2019_A13.tif'),
 PosixPath('images/17jul2019_A13.tif'),
 PosixPath('images/17jul2019_A11.tif'),
 PosixPath('images/10jul2019_A12.tif'),
 PosixPath('images/17jul2019_A12.tif'),
 PosixPath('images/10jul2019_A11.tif'),
 PosixPath('images/24jul2019_A13.tif'))

>>> from pandas import concat

>>> concat([proc_img(p) for p in path.iterdir()])
                           cc
date       plot rep
2019-07-24 A11  0    0.348066
                1    0.335986
                2    0.306889
                3    0.324631
                4    0.360818
...                       ...
           A13  5    0.322602
                6    0.318275
                7    0.294764
                8    0.229808
                9    0.306225
<BLANKLINE>
[90 rows x 1 columns]

So these are the results for the whole directory, but let's say we want to do
this in parallel.

We'll use the cpu_count function from the os module to count our processors

>>> from os import cpu_count

>>> cpu_count()
4

We'll use the Pool object from the multiprocessing module to create a simple
parallel process. We tell the Pool how many processors it should use (as many
as you have -- it does this by default, but I wanted to be explicit).

We can then map a function to some iterable using the pool. That is to say,
we can ask the pool to break an iterable up over our four processes, and run
them all at the same time.

We pass a chunksize as well -- this tell the pool to break the iterable up into
chunks of this size, and pass each one to a process. By passing this option, we
ensure that we use no more processes than needed.

We'll use the ceil function to round our chunksize up.

from multiprocessing import Pool
from math import ceil

>>> chunk = ceil(len(imgs) / cpu_count())

Again, we need to use a context manager to make sure our pool resources are
returned to the system.

>>> with Pool(cpu_count()) as pool:
...    res = concat(pool.imap_unordered(proc_img, imgs, chunksize=chunk))

>>> res.sort_index()
                           cc
date       plot rep
2019-07-10 A11  0    0.100371
                1    0.137748
                2    0.176002
                3    0.146058
                4    0.093114
...                       ...
2019-07-24 A13  5    0.302402
                6    0.310514
                7    0.267368
                8    0.281715
                9    0.295420

Let's do some timing and profiling and see what we can see.

'''


if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=False, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
