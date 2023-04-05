import keyboard
import time

"""CONFIG FOR MACROS"""
# MAIN CONTROLS
north = 'up'
south = 'down'
east = 'right'
west = 'left'
action = 'return'
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

        elif keyboard.is_pressed(attack):
            k = '1'
        elif keyboard.is_pressed(defend):
            k = '2'
        elif keyboard.is_pressed(ultimate):
            k = '3'
        elif keyboard.is_pressed(flee):
            k = '4'

        else:
            k = None

        p = window.checkMouse()
        time.sleep(0.1)

    return p, k
