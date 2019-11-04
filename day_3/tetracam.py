>>> class TetracamImage:
...
...     # thanks Kevin!
...     BANDS = ('nir', 'blue', 'green', 'yellow', 'red', 'edge')
...
...     # constructor
...     def __init__(self, path):
...         img = Image.open(path)
...         self._mtif = ImageSequence.Iterator(img)
...
...     # item access, like list[item] or dict[item]
...     def __getitem__(self, item):
...         return self._mtif[self.BANDS.index(item)].getchannel(0)
...
...     def rgb(self, r='red', g='green', b='blue'):
...         return Image.merge('RGB', (self[r], self[g], self[b]))


>>> img = TetracamImage('images/20190815_A.tif')

>>> img
<__main__.TetracamImage object at 0x7fc046b46cc0>

>>> np.array(img['red'])
array([[0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       [0, 0, 0, ..., 0, 0, 0],
       ...,
       [2, 3, 2, ..., 2, 0, 0],
       [3, 4, 3, ..., 2, 0, 0],
       [2, 3, 3, ..., 5, 0, 0]], dtype=uint8)

>>> img.rgb().show()

>>> img.rgb(r='nir', g='red', b='green').show()


    Handy, but what just happened? Let's start with classes. A class is a set of
    things with similar characteristics. Here, each TetracamImage has a path
    that sets it apart from all other TetracamImages.
