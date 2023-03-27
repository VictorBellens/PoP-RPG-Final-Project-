class Enemy:
    def __init__(self):
        self.hp = None
        self.atk = None
        self.name = None
        self.lvl = None


class Boss(Enemy):
    def __init__(self):
        Enemy.__init__(self)
