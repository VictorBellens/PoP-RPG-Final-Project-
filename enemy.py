class Enemy:
    def __init__(self):     # These are currently hard-coded
        self.hp = 100
        self.max_hp = 100
        self.atk = 5
        self.name = 'Monster'
        self.lvl = 1
        self.is_dead = False

    def _checkIsDead(self):
        if self.hp <= 0:
            self.is_dead = True

    def getResponse(self, character, action):       # str(action)[29] represents which action the user used (a/d/u/f)
        response = str(action)[29]
        print(f"response = {response}")

        if response == 'a':
            self.hp -= character.atk

        self._checkIsDead()

    def getName(self):
        return self.name


class Boss(Enemy):
    def __init__(self):     # This will be responsible for the boss attack attributes/rewards/etc.
        Enemy.__init__(self)
