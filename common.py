import keyboard
import time

""""
=====CONTROLS=====
Move up:     ↑
Move down:   ↓
Move left:   ←
Move right:  →
Action:      space
Inventory:   i
Stats:       s
Quit:        q
action_1:    1
action_2:    2
action_3:    3
action_4:    4
action_5:    5
action_6:    6
exit window: space
==================
"""


"""VARS ETC."""
log = {}

"""CONFIG FOR MACROS (DO NOT EDIT)"""
# MAIN CONTROLS
north = 'up'
south = 'down'
east = 'right'
west = 'left'
action = 'return'     # this is the only reason why we can't edit
inventory = 'i'
_quit = 'q'
stats = 's'
# ATTACK CONTROLS
attack = '1'
defend = '2'
ultimate = '3'
flee = '4'
# ITEM CONTROLS
use_item = 'u'
store_item = 'y'
# SHOP CONTROLS
buy_1 = '1'
buy_2 = '2'
buy_3 = '3'
buy_4 = '4'
buy_5 = '5'
exit_ = '6'


"""COMMON FUNCTIONS"""


def handle_input(window):
    p = None
    k = None
    while k is None and p is None:
        if keyboard.is_pressed(north):          # MAIN CONTROLS
            k = 'Up'
        elif keyboard.is_pressed(south):
            k = 'Down'
        elif keyboard.is_pressed(east):
            k = 'Right'
        elif keyboard.is_pressed(west):
            k = 'Left'
        elif keyboard.is_pressed(action):
            k = 'Return'
        elif keyboard.is_pressed(inventory):
            k = 'i'
        elif keyboard.is_pressed(_quit):
            k = 'q'
        elif keyboard.is_pressed(stats):
            k = 's'

        elif keyboard.is_pressed('space'):        # EXIT CONTROLS
            k = 'space'

        elif keyboard.is_pressed(use_item):        # ITEM CONTROLS
            k = 'u'
        elif keyboard.is_pressed(store_item):
            k = 'y'

        elif keyboard.is_pressed(attack):          # ATTACK + ITEM CONTROLS
            k = '1'
        elif keyboard.is_pressed(defend):
            k = '2'
        elif keyboard.is_pressed(ultimate):
            k = '3'
        elif keyboard.is_pressed(flee):
            k = '4'
        elif keyboard.is_pressed(buy_5):
            k = '5'
        elif keyboard.is_pressed(exit_):
            k = '6'

        else:
            k = None

        p = window.checkMouse()
        time.sleep(0.1)

    return p, k


def get_exit(obj):
    while True:
        p, k = handle_input(obj.window)
        try:
            if k == 'space' or (0 <= p.getX() <= 400 and 0 <= p.getY() <= 400):
                obj.run_flag = False
                obj.window.close()
                break
        except AttributeError:
            continue
