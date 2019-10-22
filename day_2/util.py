from copy import copy
from os import linesep, system
from pdb import set_trace
from time import sleep

from colorama import init as init_colors, Fore, Back, Style

# Colorama needs to mess with some stuff on windows before it will work
init_colors()

# exploration frame
FRAME = ((0,1), (1,1), (1,0), (1,-1), (0,-1), (-1, -1), (-1, 0), (-1, 1))

# color index
COLORS = (
    Back.BLACK,     # wall
    Back.GREEN,     # floor
    Back.BLUE,      # water
    Back.RED,       # lava
    Back.WHITE,     # passable fog
    Back.WHITE)     # impassable fog

# a drawing of a skull
SKULL = r'''

         _______
        / _   _ \
       | (_) (_) |
        \   ^   /
         |,,,,,|
         \_____/

        GAME OVER


'''

# add initial cell to HISTtory


def turn(pos, his, events, lvls):
    clear()
    draw_level(pos, his, lvls)
    tmp = events.get(pos, default)(pos, his, lvls) or pos
    his.add(pos)
    turn(tmp, his, events, lvls)


def clear():
    '''should clear the terminal on all systems -- we'll see
    '''
    system('cls||clear')


def draw_level(pos, his, lvls):
    '''draw an entire level of the cave
    '''
    res = []
    exp = explored(pos, his)
    z = pos[2] # get floor
    for y, row in enumerate(lvls[z]):
        tmp = ' ' * 30 # temporary row
        for x, val in enumerate(row):
            loc = (x, y, z) # as tuple
            if not loc in exp: # if it hasn't been explored, it's fog
                val = 4
            if loc == pos: # print an indicator if it's the current position
                cell = Fore.BLACK + '[]' + Style.RESET_ALL
            else: # everything else is a space with colored background
                cell = '  '
            tmp += (COLORS[val] + cell) # prepend correct backgroun
        tmp += Style.RESET_ALL
        res.append(tmp) # add row to result
    print()
    print((linesep).join(res)) # return string of rows joined with newlines


def explored(pos, his):
    '''update explored
    '''
    tmp = copy(his)
    tmp.add(pos)
    exp = set((pos,))
    for x, y, z in tmp:
        for x_, y_ in FRAME:
            exp.add((x + x_, y + y_, z))
    return exp


def get_val(pos, lvls):
    '''
    '''
    x, y, z = pos
    try:
        return lvls[z][y][x]
    except IndexError:
        pass


def walk(pos, his, lvls, msg):
    '''print some message, then offer a choice of directions
    '''
    if msg: # print some message, or skip it
        print(msg)
    tmp = list(pos) # copy POS as a list
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
        return walk(pos, his, lvls, '''
invalid choice
''')
    val = get_val(tmp, lvls,)
    if not val or val == 5:
        return walk(pos, his, lvls, '''
You can't go that way.
''')
    return tuple(tmp)


def default(pos, his, lvls):
    val = get_val(pos, lvls)
    if val == 1:
        return walk(pos, his, lvls, '''
An unremarkable bit of cave.
''')
    elif val == 2:
        return walk(pos, his, lvls, '''
You're standing in ankle deep water.
''')
    elif val == 3:
        game_over('''\
Ouch! Lava is hot.''')
    elif val == 4:
        return walk(pos, his, lvls, '''
The fog here is impenetrable.
''')


def game_over(msg):
    '''clear terminal, print msg with skull, return
    '''
    clear()
    print(msg)
    print(SKULL)
    input('hit enter to exit')
    exit()
