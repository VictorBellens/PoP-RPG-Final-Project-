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
    "spawn": "Welcome to the world where survival is key,\n"     # complete
             " a place you may not want to be,\n"
             " if you survive a long time you will succeed!,\n"
             "clear as many rooms and your life will be at ease",
    "before_first_kill": "You have encountered your first enemy!\n"     # complete
                         "They will get stronger the higher your level!,\n"
                         " be careful and don't get fooled, they can be quite tricky",
    "after_first_kill": "Well done on conquering your first monster!\n"     # complete
                        "Be ready, they will keep coming,\n"
                        " are you prepared to die?",
    "item_health": "You have encountered a health item!\n"      # complete
                   "This will increase your health by a\n"
                   "certain amount depending on your xp level",
    "item_max_hp": "Good one! This will increase your hp by 10. Use it wisely!",      # impl.
    "item_attack": "Cool! You can now absorb its power and have a stronger attack.",      # impl.
    "lvl_up": "Congratulations! You just leveled up, keep it up!",           # impl.
    "lvl_2_kill": "Amazing! You just killed a level 5 monster",
    "lvl_3_kill": "What a talent you are! You just killed a level 11 monster, the strongest monster out there!",
    "next_room": "You have managed to clear your first room, good job! Are you ready for the next one? It will get harder!",
    "d": "",
    "e": "",

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


def handle_input(window):       # handles the input from keyboard events
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


def get_exit(obj):      # this is the get_exit method that most of the ActionWindows use, essentially just cleans the
                        # code so that there won't be any errors
    while True:
        try:
            p, k = handle_input(obj.window)
        except graphicInterface.graphics.GraphicsError:     # handles force closing window
            obj.run_flag = False
            obj.window.close()
            break
        try:
            if k == 'space' or (0 <= p.getX() <= 400 and 0 <= p.getY() <= 400):     # click anywhere or space to close
                obj.run_flag = False
                obj.window.close()
                break
        except AttributeError:      # happens when p and k are not set (just runs again)
            continue


def get_player_profile(output_filename,  size=(50, 35)):        # gets the new player profile image
    print("Changing your player profile...\nGet ready for a photo!")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():      # camera didn't open
        print("Error: Could not open camera.")
        return

    for n in range(3):      # timer for the photo
        print(3 - n)
        time.sleep(1)

    ret, frame = cap.read()     # captures camera contents
    cap.release()

    if not ret:
        print("Error: Could not capture frame.")
        return

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    resized_image = image.resize(size, Image.ANTIALIAS)
    resized_image.save(output_filename)     # saves the image in the right dir

    print(f"Image saved successfully @ {output_filename}.")


def settings():     # settings for the game
    print("===SETTINGS===")
    change_profile = True
    print("You can change the image of your character, we do not recommend this,"
          " if you do change the picture, \nit will be saved whilst the program is running"
          " and afterwards it will be deleted.\n")

    while change_profile:
        p_change = input("Change profile (y/n): ")

        if p_change.lower() == 'y':
            get_player_profile("spriteMap/player_custom 55x55.png")
            change_profile = False
        elif p_change.lower() == 'n':
            change_profile = False
        else:
            print("\n===ERROR===\nPlease input a valid value\n")


def delete_player_sprite():     # deletes the player sprite
    if exists("spriteMap/Player_custom 55x55.png"):
        remove("spriteMap/Player_custom 55x55.png")
        print("Custom profile image deleted.")


def get_character_sprite():     # gets the character sprite
    if exists("spriteMap/Player_custom 55x55.png"):
        return "spriteMap/Player_custom 55x55.png"
    else:
        return "spriteMap/Player 55x55.png"
