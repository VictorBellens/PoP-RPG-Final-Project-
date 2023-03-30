from room import Room


class Character:    # This is responsible for the character attributes, and all methods tied to room, items, enemy, etc.
    def __init__(self):
        self.hp = 100       # these are all character attributes we can add more if we want more complexity
        self.max_hp = 100
        self.atk = None
        self.name = None
        self.gold = 100
        self.level = None
        self.to_next_level = 0/100

        self.inventory = []

        self.current_room = Room(25, 25, 0, 0, 100)     # Starting room rng, only enemy is currently implemented (nf)
        self.rooms_cleared = 0          # Create a new list attribute which contains all the previous rooms?
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

    def getShops(self):
        return self.current_room.shops

    def getShopPositions(self):
        return self.current_room.shops.values()

    def getBarriers(self):
        return self.current_room.barriers

    def getBarrierLocation(self):
        return self.current_room.barriers.values()

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

    def getNextRoom(self):      # rng will be in #room.py, the var below are only for XP level/difficulty
        item_count = 25
        enemy_count = 25
        barrier_count = 30
        shop_count = 100
        xp_level = 1

        if self.rooms_cleared % 2 == 0:      # Change this to a higher number later
            shop_count = 100

        self.current_room = Room(item_count, enemy_count, barrier_count, shop_count, xp_level)

    def performAction(self):
        if self.current_pos == self.current_room.matrix[-1]:
            print("Moving to new room...")
            self.rooms_cleared += 1
            self.getNextRoom()
            self.current_pos = self.current_room.matrix[0]

        elif self.current_pos in (eps := self.getEnemyPositions()):
            print("Enemy encountered")
            for pos in eps:
                if pos == self.current_pos:
                    current_enemy = self.getEnemies()   # this needs changing?
                    self.attackEnemy(current_enemy)
                    break

        elif self.current_pos in (ips := self.getItemPositions()):
            print("Item encountered")
            for pos in ips:
                if pos == self.current_pos:
                    item = self.getItems()
                    self.useItem(item)
                    break

        elif self.current_pos in (sps := self.getShopPositions()):
            print("Shop encountered")
            for pos in sps:
                if pos == self.current_pos:
                    shop = self.getShops()
                    self.useShop(shop)
                    break

    def attackEnemy(self, enemy):           # here is where we need to implement the attack functions.
        print("Running attack enemy method")
        self.hp -= 10

    def useItem(self, item):                # here is where we need to implement the shop functions
        print("Running use item method")
        self.hp += 10

    def useShop(self, shop):                      # here is where
        print("Running the use shop method")
        self.gold -= 10

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
