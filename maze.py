from copy import copy
from os import linesep, system
from pdb import set_trace
from time import sleep

from colorama import init as init_colors, Fore, Back, Style

# Colorama needs to mess with some stuff on windows before it will work
init_colors()

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
        [0,0,0,1,0,0,0,2,0,0],# 5
        [0,4,4,4,0,0,0,2,0,0],# 6
        [0,0,0,4,4,0,0,2,0,0],# 7
        [0,0,0,4,0,0,0,0,0,0],# 8
        [0,0,0,0,0,0,0,0,0,0] # 9
    ],#         z 2
    [# x 0 1 2 3 4 5 6 7 8 9    y
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0,0,0],# 2
        [0,0,0,0,0,0,0,0,0,0],# 3
        [0,0,0,0,0,0,0,0,0,0],# 4
        [0,0,0,0,0,0,0,0,0,0],# 5
        [0,0,0,0,0,0,0,0,0,0],# 6
        [0,0,0,0,0,0,0,0,0,0],# 7
        [0,0,0,0,0,0,0,0,0,0],# 8
        [0,0,0,0,0,0,0,0,0,0] # 9
    ]
]

# exploration frame
FRAME = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1, -1), (-1, 0), (-1, 1))

COLORS = (
    Back.BLACK,     # wall
    Back.GREEN,     # floor
    Back.BLUE,      # water
    Back.RED,       # lava
    Back.WHITE)     # fog

# a drawing of a skull
SKULL = '''\

         _______
        / _   _ \
       | (_) (_) |
        \   ^   /
         |,,,,,|
         \_____/

        GAME OVER'''

# visited cells -- we don't want to repeat
HIS = set()

# exlplored cells
EXP = set()

# initial position
POS = (2, 9, 0)

def explore():
    '''update explored
    '''
    EXP.add(POS)
    HIS.add(POS)
    for x, y in FRAME:
        tmp = (POS[0] + x, POS[1] + y, POS[2])
        EXP.add(tmp)

# explore initial position before starting
explore()

def turn():
    clear()
    explore()
    draw_level()
    EVENTS.get(POS, default)()
    turn()

def clear():
    '''should clear the terminal on all systems -- we'll see
    '''
    system('cls||clear')


def draw_level():
    '''draw an entire level of the cave
    '''
    res = []
    z = POS[2] # get floor
    for y, row in enumerate(LEVELS[z]):
        tmp = '' # temporary row
        for x, val in enumerate(row):
            loc = (x, y, z)
            for x_, y_ in FRAME:
                if get_val((x + x_, y + y_, z)) == 4:
                    val = 4
            if not loc in EXP: # if it hasn't been explored, it's fog
                val = 4
            if loc == POS: # print an indicator if it's the current position
                cell = Fore.BLACK + '[]' + Style.RESET_ALL
            else: # everything else is a space with colored background
                cell = '  '
            tmp += (COLORS[val] + cell) # prepend correct backgroun
        tmp += Style.RESET_ALL
        res.append(tmp) # add row to result
    print((linesep).join(res)) # return string of rows joined with newlines

def game_over(msg):
    '''clear terminal, print msg with skull, return
    '''
    clear()
    print(msg)
    print(SKULL)
    return

def get_val(pos):
    '''
    '''
    x, y, z = pos
    try:
        return LEVELS[z][y][x]
    except IndexError:
        pass

def walk(msg):
    '''print some message, then offer a choice of directions
    '''
    global POS
    if msg: # print some message, or skip it
        print(msg)
    tmp = list(POS) # copy POS as a list
    # wait for input
    dir = input('Will you go [n]orth, [s]outh, [e]ast or [w]est? ')
    if dir == 'n':
        tmp[1] -= 1
    elif dir == 's':
        tmp[1] += 1
    elif dir == 'w':
        tmp[0] -= 1
    elif dir == 'e':
        tmp[0] += 1
    else:
        walk('''\
invalid choice
''')
        return
    if not get_val(tmp):
        walk('''\
You can't go that way.
''')
    else: # builds up stack of invalid POS otherwise
        POS = tuple(tmp)

def default():
    val = get_val(POS)
    if val == 1:
        walk('''\
An unremarkable bit of cave.
''')
    elif val == 2:
        walk('''\
You're standing in ankle deep water.
''')
    elif val == 3:
        game_over('''\
Ouch! Lava is hot.''')
    elif val == 4:
        walk('''\
The fog here is impenetrable.
''')

def torch():
    walk('''\
You find some kind of old-timey torch on the ground. This town is full of
weirdos.
''')

def bottles():
    walk('''\
There are a bunch of those tiny plastic liquor bottles laying around here.
''')

def start():
    walk('''\
It's Halloween night and you're standing in the mouth of the cave known locally
as "Spooky Cave." You're not sure, but the name probably comes from the steam
that's always billowing out, the strange gibbering sounds that can occasionally
be heard within, and the number of people who've disappeared inside over the
years. The local authorities have made no effort whatsoever to investigate the
cave, secure the entrance, or even post a sign. For obvious reasons, you've
decided to visit the cave alone. Good thing you always carry a flashlight.
''')

def gremlins():
    print('''\
You've found the source of the gibbering -- gremlins! It looks like they're
doing some creepy stuff, but it's hard to tell.
''')
    c = input('''\
Will you try to [f]ight the gremlins, [t]alk to them, or [l]ook around? ''')
    if c == 'f':
        game_over('''\
What's wrong with you? They're tiny, and they might have been the cute kind.
You could have at least tried to talk to them. Now they're all gone. You may
still be breathing, but you're dead inside.
''')
    elif c == 't':
        walk('''\
The gremlins stare blankly at you for a moment before returning to what you now
see is some kind of adorable mischief.
''')
    elif c == 'l':
        print('''\
There's more steam here and it's warmer, but not uncomfortable. The conditions
seem to support moss that's edible for the gremlins at least.
''')
        gremlins()
    else:
        print('invalid choice')
        gremlins()

def stream():
    global POS
    print('''
The water is much deeper here, you slip, fall and are carried away by the
current.
''')
    sleep(3)
    for pos in ((5, 6, 0), (5, 7, 0), (6, 7, 0), (7, 7, 0)):
        clear()
        POS = pos
        explore()
        draw_level()
        sleep(1)
    POS = (7, 7, 1)

def thicker():
    walk('''\
The fog is getting thicker here -- visibility drops off sharply ahead.
''')

def thickest():
    walk('''\
The fog is very thick, and warm. It's beginning to seem more like steam than
fog. Either way, you can't see a thing. Tread carefully.
''')

def pit(): pass

def to_lava(): pass

EVENTS = {
    (2, 9, 0): start,
    (3, 1, 0): torch,
    (2, 2, 0): bottles,
    (5, 5, 0): stream,
    (3, 4, 1): thicker,
    (3, 5, 1): thickest,
    (1, 6, 1): to_lava,
    (3, 8, 1): pit
}

if __name__ == '__main__':
    turn()
