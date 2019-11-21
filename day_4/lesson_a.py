'''
Before we get into the applied part of today's lesson, I want to touch on some
concepts in programming. I'm not really expecting you to retain any of this,
but I do want to give you some context for the things that I do want you to
retain. "Why" is a huge part of this discussion.

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

    def foo(self, i_gross):
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
