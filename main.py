"""
===================================================================
Role-playing game final project for Principles of Programming (IE)
Authors: Victor B, Edouard P, Guy M, Mathias Z, Diana R, Alexa K

Repository: https://github.com/VictorBellens/PoP-RPG-Final-Project-
===================================================================
"""

from gameWindow import GameWindow
from common import settings


if __name__ == '__main__':
    settings()            # runs the settings for the game
    gw = GameWindow(save_log=True)      # instantiates game window object
    gw.startWindow()        # runs the main loop
