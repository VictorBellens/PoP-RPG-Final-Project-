import keyboard

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
escape = 'escape'

# ATTACK CONTROLS

# ITEM CONTROLS

# SHOP CONTROLS


def handle_input(window):
    p = None
    k = None
    while k is None and p is None:
        if keyboard.is_pressed(north):
            k = 'Up'
        elif keyboard.is_pressed(south):
            k = 'Down'
        elif keyboard.is_pressed(east):
            k = 'Right'
        elif keyboard.is_pressed(west):
            k = 'Left'
        elif keyboard.is_pressed(action):
            k = 'Return'
        elif keyboard.is_pressed('enter'):      # needs changing
            k = 'Enter'
        elif keyboard.is_pressed(inventory):
            k = 'i'
        elif keyboard.is_pressed(_quit):
            k = 'q'
        elif keyboard.is_pressed(stats):
            k = 's'
        elif keyboard.is_pressed(escape):
            k = 'escape'
        else:
            k = None

        p = window.checkMouse()

    return p, k
