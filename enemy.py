class Enemy:
    def __init__(self):     # This will be responsible for the attack attributes
        self.hp = None
        self.atk = None
        self.name = None
        self.lvl = None


class Boss(Enemy):
    def __init__(self):     # This will be responsible for the boss attack attributes/rewards/etc.
        Enemy.__init__(self)
