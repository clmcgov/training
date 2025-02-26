
'''DAY 2


    We'll start by getting atom set up and cloning the training repo.

    https://github.com/clmcgov/training

    bring up anaconda prompt and type:

cd github/training/day_2

python maze.py


    You may also want to bring up a second anaconda prompt with the ipython
    interpreter to follow along with the lesson, you'll need to navigat to the
    day_2 directly again in that window.

    Lines beginning with >>> can be pasted directly into the interpreter, along
    with any lines immediately below beginning with ...

    For example, lines 64-68 of this file can be pasted as a block directly into
    the interpreter

    Today we learn about sequences, sets, dictionaries, and functions. A main
    goal is to understand sequence indexing and concepts of mutability.


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
  File ..., line 1330, in __run
    compileflags, 1), test.globs)
  File "<doctest lesson[4]>", line 1, in <module>
    l[3]
IndexError: list index out of range


    We can set the value of items in a list by index

>>> l[1] = 9

>>> l
[1, 9, 3]


    Lists can contain lists... which can contain tuples, etc. This is
    essentially a two-band image.

>>> ll = [
... #  0       1       2
... [(0, 2), (1, 2), (2, 2)], # 0
... [(0, 1), (1, 1), (2, 1)], # 1
... [(0, 0), (1, 0), (2, 0)]] # 2


    Notice that when we bring ll up, all of the comments (#) as well as >>> and
    ... have disappeared, and the lines have been concatenated.

>>> ll
[[(0, 2), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (2, 0)]]


    We can think of ll as a matrix where we access elements in (y, x) order
    from top to bottom, left to right. This reflects that fact that the top row
    is the first element of the list, etc. Compare this to the cartesian
    coordiates at each element

>>> ll[0]
[(0, 2), (1, 2), (2, 2)]

>>> ll[1]
[(0, 1), (1, 1), (2, 1)]

>>> ll[1][2]
(2, 1)

>>> ll[1][1]
(1, 1)

>>> ll[0][2]
(2, 2)


    Lets import the maze module -- this give us access to the the maze
    "namespace."

>>> import maze


    maze is a module -- a file containing predefined names. The names in maze
    are below (ignore anything that starts with an underscore). Compare this
    with the contents of the maze.py file in this directory.

>>> dir(maze)
['Back', 'COLORS', 'EVENTS', 'FRAME', 'Fore', 'LEVELS', 'SKULL', 'START',
'Style', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
'__name__', '__package__', '__spec__', 'bottles', 'clear', 'copy', 'default',
 'draw_level', 'explored', 'game_over', 'get_val', 'gremlins', 'init_colors',
'island_floor', 'island_stream', 'linesep', 'pit', 'set_trace', 'sleep',
'start', 'stream', 'system', 'thicker', 'thickest', 'to_lava', 'torch',
'turn', 'walk']


    We can access the names in maze as attributes of the module using a dot.
    START contains the starting coordinates of the maze as (x, y, z)

>>> maze.START
(2, 9, 0)


    The LEVELS constant (in maze) contains the map -- we'll look at the first
    floor. This is basically a single-band categorical image. Enter the maze
    again and compare the first floor to this list -- you should see some
    similarities. You should be able to identify the start (START).

>>> maze.LEVELS[0]
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


    Tuples are a lot like lists:

>>> t = tuple(l)

>>> t
(1, 9, 3)


    We can create a tuple like we created the list:

>>> t = (1, 2, 3)

>>> t
(1, 2, 3)


    We can convert the tuple back to a list:

>>> list(t)
[1, 2, 3]


    We CANNOT set the values of items in a tuple. Tuples are "immutable" --
    they cannot be changed in place. This is one of the more confusing concepts
    in python, but it has some important consequences.

>>> t[2] = 9
Traceback (most recent call last):
  File ..., line 1329, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__[22]>", line 1, in <module>
    t[2] = 9
TypeError: 'tuple' object does not support item assignment


    COLORS is a constant tuple. Each element of the tuple is actually
    a constant value from the colorama module (see util.py). Constants are
    indicated by all capitol letters in Python. It's not very important what
    these are, just know that they tell your terminal to print in different
    colors.

>>> maze.COLORS
('\\x1b[40m', '\\x1b[42m', '\\x1b[44m', '\\x1b[41m', '\\x1b[47m', '\\x1b[47m')


    We can use the "enumerate" function to generate tuples of (index, value)
    from COLORS. By default, this function returns a "generator," so we need
    to wrap it in a call to tuple. A generator is an object that returns values
    on demand, rather than all at once -- this is a memory optimization that
    we can ignore for now. Note that the index of each color corresponds to one
    of the integer values in LEVELS. We can get the color of any square s in the
    maze with COLORS[s].

>>> tuple(enumerate(maze.COLORS))
((0, '\\x1b[40m'),
(1, '\\x1b[42m'),
(2, '\\x1b[44m'),
(3, '\\x1b[41m'),
(4, '\\x1b[47m'),
(5, '\\x1b[47m'))


    Generally, constants should be immuatble types -- if they can change, then
    they aren't constant. Python does not enforce the concept of a constant in
    any way, so we need to be disciplined about this. The all caps thing is
    really just a convention to indicate to other people that something should
    be considered constant. You might wonder why LEVELS is a list -- maybe it
    shouldn't be but I wanted it to look like the the NumPy arrays that you'll
    see later.


    Let's take a quick break to talk about functions. A function is a thing that
    does something -- helpful, right? Specifically, a function takes zero or
    more arguments, and returns 0 or more things. In some circles, a function
    that returns nothing is called a procedure. Here's a simple function:

>>> def myfunc(arg1, arg2):         # definition with argument specification
...     """add two values together  # docstring -- optional documentation
...     """
...     val = arg1 + arg2           # body
...     return val                  # return statement


    When you "pass" a set of arguments to a function, you are "calling" it --
    asking it to do whatever it does with them.

>>> myfunc(1, 2)
3


    Next, we'll talk about sets. A set in Python is just like a set in math -- a
    collection of unordered, unique things. Consider the list c:

>>> c = [1, 2, 2, 3, 3, 3]

>>> len(c)
6


    Now consider the set c:

>>> set(c)
{1, 2, 3}


    This might look ordered, and in fact, Python 3 sets do remember item
    insertion order, but this isn't really a feature, just a fact -- sets are
    intended to be unordered. We can see this if we attmpt to index a set.

>>> c = set(c)

>>> c[1]
Traceback (most recent call last):
  File ..., line 1329, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__[28]>", line 1, in <module>
    c[1]
TypeError: 'set' object does not support indexing


    The "his" argument to each event function expects a set of visited
    coordinates. We wouldn't want to use a list for this, because we don't
    really care how many times a cell was visited, or in what order. We just
    want to know if it's ever been visited.


    A dictionary is just like a set (the syntax is similar), except that each
    item is a key mapped to some value.

>>> d = {'cat': 'Burt', 'dog': 'Hess'}


    We can add a new value with the same syntax we use for lists:

>>> d['bird'] = 'Polly'

>>> d
{'cat': 'Burt', 'dog': 'Hess', 'bird': 'Polly'}


    If we set the same key again, we just change the value -- keys are unique.

>>> d['dog'] = 'Dina'

>>> d
{'cat': 'Burt', 'dog': 'Dina', 'bird': 'Polly'}


    We can ask for the keys of a dictionary, or its values, or both:

>>> list(d.keys())
['cat', 'dog', 'bird']

>>> list(d.values())
['Burt', 'Dina', 'Polly']

>>> list(d.items())
[('cat', 'Burt'), ('dog', 'Dina'), ('bird', 'Polly')]


    EVENTS contains a listing of event functions mapped to a set of coordinates.
    If we feed the starting coordinates into the EVENTS dictionary, we get the
    start function (look in maze.py, you should recognize it):

>>> maze.START
(2, 9, 0)

>>> maze.EVENTS[maze.START]
<function start at ...>


    This is where mutability counts. If we were to attempt to assign coordinate
    lists as keys instead of tuples, we'd get an exception about lists not
    being hashable -- we need to use an immutable type like a tuple.

>>> d = {['a_list']: 'fails'}
Traceback (most recent call last):
  File ...., line 1330, in __run
    compileflags, 1), test.globs)
  File "<doctest __main__[41]>", line 1, in <module>
    d = {['a_list']: 'fails'}
TypeError: unhashable type: 'list'


    Hopefully by now you have some idea of how the maze actually works. Feel
    free to dig into the source code and bring any questions you have to me.
    maze.py is the top level code -- it may be clear to you, but it's fine if
    it's not. util.py contains the guts of the maze, and will be a little harder
    to work out, but may be rewarding.
'''

if __name__ == '__main__':
    from doctest import testmod, NORMALIZE_WHITESPACE, ELLIPSIS, \
        IGNORE_EXCEPTION_DETAIL
    testmod(verbose=True, optionflags=NORMALIZE_WHITESPACE | ELLIPSIS
        | IGNORE_EXCEPTION_DETAIL)
