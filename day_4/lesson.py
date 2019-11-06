'''

    Let's wrap this whole thing into a function

>>> def img_to_cc(path):
...     """calculate canopy cover from a tetracam multi-tiff file (2019 only)
...     """
...     img = Image.open(path)                          # get image file object
...     mtif = ImageSequence.Iterator(img)              # it's a multi-tiff
...     res = ndvi(                                     # get ndvi
...         nir=np.array(get_band(mtif, 'nir')),        # don't keep bands
...         red=np.array(get_band(mtif, 'red')))        #   in memory
...     res = res[np.isfinite(res)]                     # remove nan/inf
...     th = threshold_otsu(res)                        # get threshold
...     res = np.where(res > th, 1, 0).astype(np.uint8) # classify
...     return res.sum() / res.size                     # get scalar cover

>>> img_to_cc('images/20190815_A.tif').round(5)
0.74309


    Cool, it works! Now let's say we want to automate this a little more and
    iterate over the whole directory. We'll need to be able to extract some
    information from the file names so we can associate canopy cover with
    other usefule columns.

    To iterate, we'll use pathlib.

>>> from pathlib import Path

>>> path = Path('images')

>>> list(path.iterdir())
[PosixPath('images/20190815_B.tif'), PosixPath('images/20190815_C.tif'),
 PosixPath('images/20190815_A.tif')]


    That's all of our images. To get the name of each image without a file
    extension, we can use the stem property of each Path object

>>> [p.stem for p in path.iterdir()]
['20190815_B', '20190815_C', '20190815_A']


    What you just saw is called a list comprehension It's a sort of compressed
    loop syntax that can be very useful, sometimes faster, and always
    convenient. It's equivalent to:

>>> tmp = []

>>> for p in path.iterdir():
...     tmp.append(p.stem)

>>> tmp
['20190815_B', '20190815_C', '20190815_A']


    To parse the filenames, we can use the string split method with multiple
    assignment

>>> date, plot = tmp[0].split('_')

>>> date
'20190815'

>>> plot
'B'


    We'll just go ahead and turn the date into a Pandas Timestamp -- more on
    Pandas later

>>> import pandas as pd

>>> date = pd.Timestamp(date)

>>> date
Timestamp('2019-08-15 00:00:00')


    Now we'll create a function that takes a path, extracts plot and timestamp,
    and gets canopy cover.

>>> def process_img(path):
...     date, plot = path.stem.split('_')
...     date = pd.Timestamp(date)
...     cover = img_to_cc(path)
...     return date, plot, cover


    Multiple returns will end up as a tuple. Let's see what happens when we
    use our new function in a list comprehension.

>>> tmp = [process_img(p) for p in path.iterdir()]

>>> tmp
[(Timestamp('2019-08-15 00:00:00'), 'B', 0.76778564453125),
 (Timestamp('2019-08-15 00:00:00'), 'C', 0.7331199645996094),
 (Timestamp('2019-08-15 00:00:00'), 'A', 0.7430923461914063)]


    That looks kind of like a table -- maybe we can pass it to the Pandas
    DataFrame constructor along with some column names

>>> df = pd.DataFrame(tmp, columns=['date', 'plot', 'cover'])

>>> df
        date plot     cover
0 2019-08-15    B  0.767786
1 2019-08-15    C  0.733120
2 2019-08-15    A  0.743092


    Setting an index does a few things, but for now it just makes it look nicer

>>> df = df.set_index(['date', 'plot'])

>>> df
                    cover
date       plot
2019-08-15 B     0.767786
           C     0.733120
           A     0.743092


    Whew, we've come a long way. Let's wrap all that up in another function
    before we start forgetting things.

>>> def process_img_dir(path):
...     path = Path(path)
...     res = []
...     for p in path.iterdir():
...         res.append(process_img(p))
...     res = pd.DataFrame(res, columns=['date', 'plot', 'cover'])
...     return res.set_index(['date', 'plot'])

>>> process_img_dir('images')
                    cover
date       plot
2019-08-15 B     0.767786
           C     0.733120
           A     0.743092


    Well that's pretty neat, but what if we're still not happy? What if this
    directory of three images was just an example for test purposes? What if
    we have a powerful server with loads of rams and lots of processors? What
    if we want to be able to rip through tons of images at once using all of
    that power? Multiprocessing is the answer.

    We'll have to define this function in a module to use it in parallel.

>>> from tetracam import mproc_img_dir

>>> df = mproc_img_dir(path)

>>> df
                    cover
date       plot
2019-08-15 B     0.767786
           C     0.733120
           A     0.743092


    Finally, let's dump the dataframe to a CSV

>>> df.to_csv('output.csv')



'''

if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=True, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
