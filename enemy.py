import random


class Enemy:
    def __init__(self, chr_lvl, *args):     # handles the enemy methods
        self.hp = 100 * chr_lvl  # DEBUG
        self.max_hp = 100 * chr_lvl
        self.atk = 5 * chr_lvl
        self.name = 'Monster'
        self.lvl = chr_lvl
        self.is_dead = False
        self.no_attack_for = 0
        self.location = args[0]     # location as args[0] as some enemies are dead
        self.sprite_window = self.__getMapImage()       # different sprite sizes for map/window
        self.sprite_action_window = self.__getWindowImage()

    def __getMapImage(self):  # takes the enemy level, finds the image corresponding enemy level, then returns the image
        filename = None

        if self.lvl < 5:
            filename = 'spriteMap/Green Monster 55x55.png'
        elif 5 <= self.lvl < 10:
            filename = 'spriteMap/PurpleMonst2 55x55.png'
        elif self.lvl > 10:
            filename = 'spriteMap/Red Monster 55x55.png'

        return filename

    def __getWindowImage(self):
        filename = None

        if self.lvl < 5:
            filename = 'spriteActionWindow/Green Monster 148x148.png'
        elif 5 <= self.lvl < 10:
            filename = 'spriteActionWindow/PurpleMonst2 148x148.png'
        elif self.lvl > 10:
            filename = 'spriteActionWindow/Red Monster 148x148.png'

        return filename

    def checkIsDead(self):      # checks if the enemy is dead
        if self.hp <= 0:
            self.is_dead = True

    def getResponse(self, character, action):   # gets the response to the character action
        response = str(action)[29]      # Represents which action the user used (a/d/u/f)
        chance = random.random()

        if self.no_attack_for != 0:     # checks if the player is defended
            self.no_attack_for -= 1
            return 'defended', 'green'

        else:
            if response == 'a':     # retaliates with attack
                if chance > 0.3:
                    character.hp -= self.atk
                    return f'-{self.atk} HP', 'red'
                else:
                    return 'Missed', 'green'

            elif response == 'd':       # retaliates with attack
                character.hp -= self.atk

                if character.is_shielded:
                    character.is_shielded = False
                    rounds = random.randint(1, 3)
                    self.no_attack_for = rounds

                return f'-{self.atk} HP', 'red'

            elif response == 'u':       # checks if the user can use ultimate, if so, then uses, otherwise, it fails.
                if character.ultimate_available != 0:
                    character.ultimate_available -= 1
                    self.hp -= character.ultimate_attribute

                    return f'Ultimate', 'green'

                else:
                    character.hp -= self.atk
                    return f'-{self.atk} HP', 'red'

            elif response == 'f':       # if the user has fled, there is no response from the enemy
                pass

            else:   # if the response is not valid, meaning the objects are saved in a different format.
                raise Exception("The game needs to be changed for your device (see the documentation)")

            return 'response', 'green'

    def getName(self):      # returns the name of the enemy (0 implementation)
        return self.name
