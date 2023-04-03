import random


class Enemy:
    def __init__(self, chr_lvl):
        self.hp = 100 * chr_lvl      # DEBUG
        self.max_hp = 100 * chr_lvl
        self.atk = 5 * chr_lvl
        self.name = 'Monster'
        self.lvl = chr_lvl
        self.is_dead = False
        self.no_attack_for = 0

    def checkIsDead(self):
        if self.hp <= 0:
            self.is_dead = True

    def getResponse(self, character, action):       # str(action)[29] represents which action the user used (a/d/u/f)
        response = str(action)[29]
        chance = random.random()

        if self.no_attack_for != 0:
            self.no_attack_for -= 1
            return 'defended', 'green'

        else:
            if response == 'a':
                if chance > 0.3:
                    character.hp -= self.atk
                    return f'-{self.atk} HP', 'red'
                else:
                    return 'Missed', 'green'

            elif response == 'd':
                character.hp -= self.atk

                if character.is_shielded:
                    character.is_shielded = False
                    rounds = random.randint(1, 3)
                    self.no_attack_for = rounds

                return f'-{self.atk} HP', 'red'

            elif response == 'u':
                if character.ultimate_available != 0:
                    character.ultimate_available -= 1
                    self.hp -= character.ultimate_attribute

                    return f'Ultimate', 'green'

                else:
                    character.hp -= self.atk
                    return f'-{self.atk} HP', 'red'

            elif response == 'f':
                pass

            else:
                raise Exception("The game needs to be changed for your device (see the documentation)")

            return 'response', 'green'

    def getName(self):
        return self.name


class Boss(Enemy):
    def __init__(self, character_level):     # This will be responsible for the boss attack attributes/rewards/etc.
        Enemy.__init__(self, character_level)
