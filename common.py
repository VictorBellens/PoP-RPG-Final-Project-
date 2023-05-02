import keyboard
import time
import cv2

from PIL import Image
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
    # Open the camera (0 is the default camera index)
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Capture a frame
    ret, frame = cap.read()

    # Release the camera resource
    cap.release()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        return

    # Convert the OpenCV image (numpy array) to a PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Resize the image
    resized_image = image.resize(size, Image.ANTIALIAS)

    # Save the resized image
    resized_image.save(output_filename)

    print(f"Image captured and resized successfully. Saved as {output_filename}.")
