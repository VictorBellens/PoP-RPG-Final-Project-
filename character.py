from room import Room


class Character:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.atk = None
        self.inventory = []
        self.name = None

        self.level = None
        self.to_next_level = 0/100

        self.gold = 100

        self.current_room = None
        self.rooms_cleared = 0
        self.current_pos = [0, 0]

    def getCurrentPos(self):
        return self.current_pos

    def shop(self):  # likely will be moved to room class
        pass

    def getHp(self):
        return self.hp, self.max_hp

    def getGold(self):
        return self.gold

    def getRoomNumber(self):
        return self.rooms_cleared

    def getEnemyPositions(self):
        return self.current_room.enemies.values()

    def getEnemies(self):
        return self.current_room.enemies.items()

    def getItemPositions(self):
        return self.current_room.items.values()

    def getItems(self):
        return self.current_room.items.items()

    def getXp(self):
        return self.level

    def moveNorth(self):
        self.newPos(-1, 0)

    def moveSouth(self):
        self.newPos(1, 0)

    def moveEast(self):
        self.newPos(0, -1)

    def moveWest(self):     # (self, item_count, enemy_count, barrier_count, shop_count, xp_level):
        self.newPos(0, 1)

    def getNextRoom(self):
        item_chance = None
        enemy_count = None
        barrier_count = None
        shop_count = None
        xp_level = None

        if self.rooms_cleared > 2:      # Change this to a higher number later
            shop_count = 100

    def performAction(self):
        if self.current_pos == self.current_room.matrix[-1]:
            print("Moving to new room...")
            self.rooms_cleared += 1
            self.current_room = Room(0, 0, 0, 0, 0)         # not implemented
            self.current_pos = self.current_room.matrix[0]

        elif self.current_pos in (ep := self.getEnemyPositions()):
            print("Enemy encountered")
            for pos in ep:
                if pos == self.current_pos:
                    current_enemy = self.getEnemies()
                    self.attackEnemy(current_enemy)
                    break

        elif self.current_pos in self.getItemPositions():
            print("Item encountered")

    def attackEnemy(self, enemy):           # here is where we need to implement the attack functions.
        pass

    def newPos(self, x, y):
        new_x, new_y = self.current_pos
        new_x += x
        new_y += y
        if [new_x, new_y] not in self.current_room.matrix:
            print("Position not possible")  # RETURN AN ERROR FOR THE WINDOW
        else:
            self.current_pos = [new_x, new_y]

    def viewInventory(self):
        pass