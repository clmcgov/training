# https://github.com/clmcgov/training
# CTRL+SHIFT+P

'''DAY 2


We'll start by getting atom set up and cloning the training repo.


today we learn about sequences, sets, dictionaries, and functions. A main goal
is to understand sequence indexing and concepts of mutability.


    First, we create a list

>>> l = [1, 2, 3]


    We can access elements of a list by position. Note that we start counting at
    zero. Non-existent positions raise exceptions.

>>> l[0]
1

>>> l[1]
2

>>> l[3]
Traceback (most recent call last):
  File "/home/cullen/miniconda3/envs/dev/lib/python3.6/doctest.py", line 1330, in __run
    compileflags, 1), test.globs)
  File "<doctest lesson[4]>", line 1, in <module>
    l[3]
IndexError: list index out of range


    Tuples are a lot like lists:

>>> t = tuple(l)

>>> t
(1, 2, 3)

>>> t[2]
3


    We can create a tuple like we created the list:

>>> t = (1, 2, 3)

>>> t[2]
3


    We can convert the tuple back to a list:

>>> list(t)
[1, 2, 3]


    Lists can contain lists... which can contain tuples, etc. This is
    essentially a two-band image.

>>> l2 = [
... #  0       1       2
... [(0, 2), (1, 2), (2, 2)], # 0
... [(0, 1), (1, 1), (2, 1)], # 1
... [(0, 0), (1, 0), (2, 0)]] # 2

>>> l2
[[(0, 2), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (2, 0)]]


    We can think of l2 as a matrix where we access elements in (y, x) order
    from top to bottom, left to right. Compare this to the cartesian
    coordiates at each element

>>> l2[0]
[(0, 2), (1, 2), (2, 2)]

>>> l2[1]
[(0, 1), (1, 1), (2, 1)]

>>> l2[1][2]
(2, 1)

>>> l2[1][1]
(1, 1)

>>> l2[0][2]
(2, 2)


    Now bring up the first level of the maze. Don't fall into the water!

    Look at LEVELS in maze.py and COLORS in util.py

>>> import maze
>>> from pprint import pprint

>>> pprint(maze.LEVELS[0])
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
 [0, 2, 2, 2, 2, 2, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 2, 2, 2, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]


    COLORS is a tuple of constants. Each element of the tuple is actually
    a constant value from the colorama module. Constants are indicated by
    all capitol letters in Python. It's not very important what these are,
    just know that they tell your terminal to print in different colors

    Now we'll make a function to play around with the colors

>>> def colors(val):
...     print(maze.COLORS[val])


    "def" says we're defining a function.

    "colors" is the name of the function.

    "








'''
