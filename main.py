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
    # settings()
    gw = GameWindow(save_log=True)
    gw.startWindow()
