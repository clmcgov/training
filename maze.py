from copy import copy
from os import linesep, system
from time import sleep

from colorama import init as init_colors, Fore, Back, Style

init_colors()

# ^
# N
LEVELS = [#     z 0
    [# x 0 1 2 3 4 5 6 7 8 9    y
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,1,1,0,0,0,0,0,0],# 1
        [0,0,1,1,0,0,0,0,0,0],# 2
        [0,0,1,0,0,0,0,0,0,0],# 3
        [0,0,1,0,0,0,0,0,0,0],# 4
        [0,3,3,3,3,0,0,0,0,0],# 5
        [0,0,1,0,3,0,0,0,0,0],# 6
        [0,0,1,0,3,3,3,2,0,0],# 7
        [0,0,1,0,0,0,0,0,0,0],# 8
        [0,0,1,0,0,0,0,0,0,0] # 9
    ],#         z 1
    [# x 0 1 2 3 4 5 6 7 8 9    y
        [0,0,0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0,0,0],# 1
        [0,0,0,0,0,0,0,0,0,0],# 2
        [0,0,0,0,0,0,0,0,0,0],# 3
        [0,0,0,0,0,0,0,0,0,0],# 4
        [0,0,0,0,0,0,0,0,0,0],# 5
        [0,0,0,0,0,0,0,0,0,0],# 6
        [0,0,0,0,0,0,0,0,0,0],# 7
        [0,0,0,0,0,0,0,0,0,0],# 8
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
    Back.BLACK      # wall
    Back.GREEN,     # floor
    Back.MAGENTA,   # hole
    Back.BLUE,      # water
    Back.RED,       # lava
    Back.WHITE)     # fog

SKULL = '''\

         _______
        / _   _ \
       | (_) (_) |
        \   ^   /
         |,,,,,|
         \_____/

        GAME OVER'''

HIS = []

POS = (2, 9, 0)

EXP = set()

explore(POS)

def clear():
    os.system('cls||clear')

def draw_cell(loc, pos, exp):
    if not loc in exp:
        val = 5
    if loc == pos:
        cell = Fore.BLACK + '[]' + Style.RESET_ALL
    else:
        cell = '  '
    return COLORS[val] + cell

def draw_level(levels, pos, exp):
    z = pos[2]
    for y, row in enumerate(levels[z]):
        tmp = []
        for x, val in enumerate(row):
            loc = (x, y, z)
            tmp.append(draw_cell(loc, pos, exp))
        res.append(''.join(tmp))
    res = [row.append(Style.RESET_ALL) for row in res]
    return (linesep).join(res)

def explore(pos):
    EXP.add(pos)
    for x, y in FRAME:
        tmp = (pos[0] + x, POS[1] + y, z)
        exp.add(tmp)

def game_over(msg):
    clear()
    print(msg)
    print(SKULL)
    return

def get_val(pos):
    x, y, z = pos
    return LEVELS[z][y][x]

def walk(msg):
    if msg:
        print(msg)
    print()
    tmp = list(POS)
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
        walk('invalid choice')
    POS = tmp

def default():
    val = get_val(POS)
    if val == 1:
        walk('''
An unremarkable bit of cave.'''
    elif val == 2:
        POS[2] += 1
        if get_val(POS) == 0:
            game_over('''
You've fallen into a bottomless pit.'''
        else:
            pass
    elif val == 3:
        walk('''
You're standing in ankle deep water.''',
    elif val == 4:
        game_over('''
Why would you walk into lava?'''
    elif val == 5:
        walk('''
The fog here is impenetrable.''')

def start():
    walk('''\
It's Halloween night and you're standing in the mouth of the cave known locally
as "Spooky Cave." You're not sure, but the name probably comes from the steam
that's always billowing from the cave, the strange gibbering sounds that can
occasionally be heard within, and the number of people who've disappeared inside
over the years. The local authorities have made no effort whatsoever to
investigate the cave, secure the entrance, or even post a sign. For obvious
reasons, you've decided to visit the cave alone. Good thing you always carry a
flashlight.''')

def gremlins():
    print('''
You've found the source of the gibbering -- gremlins! It seems like they're
doing some creepy stuff.''')
    c = input('''
Will you try to [f]ight the gremlins, [t]alk to them, or [l]ook around? ''')
    if c == 'f':
        game_over('''
What\'s wrong with you? They're tiny, and they might have been the cute kind.
Now they're all gone. You may still be breathing, but you're dead inside.''')
    elif c == 't':
        walk(pos, '''
The gremlins stare blankly at you for a moment before returning to what you now
see is some kind of adorable mischief''')
    elif c == 'l':
        print('''
There's more steam here and it's warmer, but not uncomfortable. The conditions
seem to support moss that's edible for the gremlins at least''')
        gremlins()
    else:
        print('invalid choice')
        gremlins()
