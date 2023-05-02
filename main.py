"""
===================================================================
Role-playing game final project for Principles of Programming (IE)
Authors: Victor B, Edouard P, Guy M, Mathias Z, Diana R, Alexa K

Repository: https://github.com/VictorBellens/PoP-RPG-Final-Project-
===================================================================
"""

from gameWindow import GameWindow


if __name__ == '__main__':
    gw = GameWindow(save_log=True, change_profile=False)
    gw.startWindow()
