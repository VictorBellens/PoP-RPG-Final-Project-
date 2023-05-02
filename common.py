import keyboard
import time
import cv2

from PIL import Image
from os import remove
from os.path import exists
import graphicInterface.graphics

"""VARS"""
log = {}
narrative = {
    "spawn": "Welcome to the world!",       # MISC
    "before_first_kill": "I have aids",
    "after_first_kill": "and the clap",
    "item_health": "You have encountered a health item!"
                   "This will increase your health by a"
                   "certain amount depending on your xp level",
    "item_max_hp": "",
    "item_attack": "",
}


"""CONFIG FOR MACROS"""
# MAIN CONTROLS
north = 'up'
south = 'down'
east = 'right'
west = 'left'
action = 'space'       # DO NOT EDIT
inventory = 'i'
_quit = 'q'
stats = 's'
exit_window = 'space'  # DO NOT EDIT

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
exit_shop = '6'


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
        elif keyboard.is_pressed('return'):
            k = 'return'
        elif keyboard.is_pressed(inventory):
            k = 'i'
        elif keyboard.is_pressed(_quit):
            k = 'q'
        elif keyboard.is_pressed(stats):
            k = 's'
        elif keyboard.is_pressed(exit_window):        # EXIT CONTROLS
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
        elif keyboard.is_pressed(exit_shop):
            k = '6'

        else:
            k = None

        p = window.checkMouse()
        time.sleep(0.1)

    return p, k


def get_exit(obj):
    k, p = None, None
    while True:
        try:
            p, k = handle_input(obj.window)
        except graphicInterface.graphics.GraphicsError:     # handles force closing window
            print("TOUCHED")
            obj.run_flag = False
            obj.window.close()
            break
        try:
            if k == 'space' or (0 <= p.getX() <= 400 and 0 <= p.getY() <= 400):     # click anywhere or space to close
                obj.run_flag = False
                obj.window.close()
                break
        except AttributeError:      # happens when p and k are not set
            continue


def get_player_profile(output_filename,  size=(50, 50)):
    print("Changing your player profile...\nGet ready for a photo!")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    for n in range(3):
        print(3 - n)
        time.sleep(1)

    print("Capturing image!")
    ret, frame = cap.read()
    print("Image captured!")
    cap.release()

    if not ret:
        print("Error: Could not capture frame.")
        return

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    resized_image = image.resize(size, Image.ANTIALIAS)
    resized_image.save(output_filename)

    print(f"Image captured and resized successfully. Saved as {output_filename}.")


def settings():
    print("===SETTINGS===")
    change_profile = True

    while change_profile:
        p_change = input("Change profile (y/n): ")

        if p_change.lower() == 'y':
            get_player_profile("spriteMap/player_custom 55x55.png")
            change_profile = False
        elif p_change.lower() == 'n':
            change_profile = False
        else:
            print("\n===ERROR===\nPlease input a valid value\n")

    return change_profile


def delete_player_sprite():
    if exists("spriteMap/Player_custom 55x55.png"):
        remove("spriteMap/Player_custom 55x55.png")
        print("Custom profile image deleted.")


def get_character_sprite():
    if exists("spriteMap/Player_custom 55x55.png"):
        return "spriteMap/Player_custom 55x55.png"
    else:
        return "spriteMap/Player 55x55.png"
