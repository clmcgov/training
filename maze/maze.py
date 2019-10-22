from util import *

def start(pos, his, lvls):
    return walk(pos, his, lvls, '''
It's Halloween night and you're standing in the mouth of the cave known locally
as "Spooky Cave." You're not sure, but the name probably comes from the steam
that's always billowing out, the strange gibbering sounds that can occasionally
be heard within, and the number of people who've disappeared inside over the
years. The local authorities have made no effort whatsoever to investigate the
cave, secure the entrance, or even post a sign. For obvious reasons, you've
decided to visit the cave alone. Good thing you always carry a flashlight.
''')


def bottles(pos, his, lvls):
    return walk(pos, his, lvls, '''
There are a bunch of those tiny plastic liquor bottles laying around here.
''')


def torch(pos, his, lvls):
    return walk(pos, his, lvls, '''
You find some kind of old-timey torch on the ground. This town is strange.
''')


def stream(pos, his, lvls):
    print('''
The water is much deeper here, you slip, fall and are carried away by the
current.
''')
    his.add(pos)
    sleep(3)
    for pos in ((5, 6, 0), (5, 7, 0), (6, 7, 0), (7, 7, 0)):
        clear()
        his.add(pos)
        draw_level(pos, his, lvls)
        sleep(1)
    return (7, 7, 1)


def gremlins(pos, his, lvls, intro=True):
    if pos in his:
        return walk(pos, his, lvls, '''
The gremlins are still doing gremlin stuff.
''')
    if intro:
        print('''
You've found the source of the gibbering -- gremlins! It looks like they're
doing some creepy stuff, but it's hard to tell.
''')
    c = input('''\
Will you try to [f]ight the gremlins, [t]alk to them, or [l]ook around?
''')
    if c == 'f':
        game_over('''
Seriously? They're tiny, and they might have been the cute kind.
You could have at least tried to talk to them. Now they're all gone. You may be
breathing, but you're dead inside.
''')
    elif c == 't':
        return walk(pos, his, lvls, '''
The gremlins stare blankly at you for a moment before returning to what you now
see is some kind of adorable mischief.
''')
    elif c == 'l':
        print('''
There's more steam here and it's warmer, but not uncomfortable. The conditions
support a moss that the gremlins must be surviving on.
''')
        return gremlins(pos, his, lvls, False) # skip the gremlin intro
    else:
        print('invalid choice')
        return gremlins(pos, his, lvls, False) # skip intro


def thicker(pos, his, lvls):
    return walk(pos, his, lvls, '''
The fog is getting thicker here -- visibility drops off sharply ahead.
''')


def thickest(pos, his, lvls):
    return walk(pos, his, lvls, '''
The steam is very thick, and much warmer. You can't see a thing -- tread
carefully!
''')


def pit(pos, his, lvls):
    game_over('''
You've fallen into a bottomless pit. In fact, you're still falling.
''')


def to_lava(pos, his, lvls):
    print('''
You've fallen into a hole!
''')
    sleep(3)
    return (2, 6, 2)


def island_floor(pos, his, lvls):
    return walk(pos, his, lvls, '''
You're standing on a ledge above a lake of lava. You can see a skeleton here
and there. I guess we know where everyone disappeared to.
''')


def island_stream(pos, his, lvls):
    return walk(pos, his, lvls, '''
Some of the water from above is flowing into the lava -- that explains the
steam.
''')


# starting cell
START = (2, 9, 0)


# maze events
EVENTS = {
    START: start,
    (3, 1, 0): torch,
    (2, 2, 0): bottles,
    (5, 5, 0): stream,
    (3, 4, 1): thicker,
    (3, 5, 1): thickest,
    (2, 6, 1): to_lava,
    (3, 8, 1): pit,
    (4, 3, 1): gremlins,
    (1, 7, 2): island_floor,
    (2, 7, 2): island_floor,
    (3, 7, 2): island_floor,
    (1, 6, 2): island_floor,
    (2, 6, 2): island_floor,
    (3, 6, 2): island_floor,
    (1, 4, 2): island_floor,
    (2, 4, 2): island_floor,
    (3, 4, 2): island_floor,
    (1, 5, 2): island_stream,
    (2, 5, 2): island_stream,
    (3, 5, 2): island_stream,
}


# ^
# N
LEVELS = [#     z 0
    [# x 0 1 2 3 4 5 6 7 8 9    y
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,1,1,0,0,0,0,0,0],# 1
        [0,0,1,1,0,0,0,0,0,0],# 2
        [0,0,1,0,0,0,0,0,0,0],# 3
        [0,0,1,0,0,2,0,0,0,0],# 4
        [0,2,2,2,2,2,0,0,0,0],# 5
        [0,0,1,0,0,2,0,0,0,0],# 6
        [0,0,1,0,0,2,2,2,0,0],# 7
        [0,0,1,0,0,0,0,0,0,0],# 8
        [0,0,1,0,0,0,0,0,0,0] # 9
    ],#         z 1
    [# x 0 1 2 3 4 5 6 7 8 9    y
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0,0,0],# 1
        [0,0,0,1,1,0,0,2,0,0],# 2
        [0,0,0,1,1,1,1,2,0,0],# 3
        [0,0,0,1,0,0,0,2,0,0],# 4
        [0,5,5,4,5,0,0,2,0,0],# 5
        [0,5,4,4,5,5,0,2,0,0],# 6
        [0,5,5,4,4,5,0,2,0,0],# 7
        [0,0,5,4,5,5,0,0,0,0],# 8
        [0,0,5,5,5,0,0,0,0,0] # 9
    ],#         z 2
    [# x 3 1 2 3 4 5 6 7 8 9    y
        [3,3,3,3,3,3,3,3,3,3],# 3
        [3,3,3,3,3,3,3,3,3,3],# 3
        [3,3,3,3,3,3,3,3,3,3],# 2
        [3,3,3,3,3,3,3,3,3,3],# 3
        [0,1,1,1,3,3,3,3,3,3],# 4
        [0,2,2,2,3,3,3,3,3,3],# 5
        [0,1,1,1,3,3,3,3,3,3],# 6
        [0,1,1,1,3,3,3,3,3,3],# 7
        [3,3,3,3,3,3,3,3,3,3],# 8
        [3,3,3,3,3,3,3,3,3,3] # 9
    ]
]


if __name__ == '__main__':
    turn(START, set((START,)), EVENTS, LEVELS)
