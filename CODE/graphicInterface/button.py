# button.py from PoP with modifications
from graphics import *


class Button:
    def __init__(self, win, center, width, height, label, action, *args):
        # Creates a rectangular button, eg:
        # qb = Button(myWin, centerPoint, width, height, 'Quit')

        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1, p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

        try:                                                        # Added a keypress handler
            self.key = args[0]
        except IndexError:
            print(f"{label} key not configured")
        self.active = None                                          # added active to __init__
        self.action = action                                        # added action

    def clicked(self, p):                                           # Added error handling
        try:
            return (self.xmin <= p.getX() <= self.xmax and          # removed 'if button active and'
                    self.ymin <= p.getY() <= self.ymax)
        except AttributeError:
            return False

    def pressed(self, k):                                           # Added error handling
        try:
            return self.key == k
        except AttributeError:
            return False

    def getLabel(self):
        # Returns the label string of this button.
        return self.label.getText()

    def activate(self):
        # Sets this button to 'active'.
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        # Sets this button to 'inactive'.
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = False

    def getAction(self):                                          # added getAction()
        return self.action
