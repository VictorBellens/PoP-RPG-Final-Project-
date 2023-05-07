from room import Room
from actionWindows import *
from time import time

from common import narrative, get_character_sprite


class Character:  # This is responsible for the character attributes, and all methods tied to room, items, enemy, etc.
    def __init__(self):
        self.max_hp = 100
        self.hp = self.max_hp
        self.atk = 10
        # self.name = None          # 0 implementation
        self.gold = 100

        self.gold_accumulated = 0
        self.enemies_killed = 0
        self.level = 1
        self.to_next_level = 0 / 100  # xp needed for next level
        self.is_shielded = False

        self.health_item, self.max_hp_item, self.attack_item = True, True, True  # for the narrative prompts
        self.lvl_2_enemy, self.lvl_3_enemy = False, False

        self.ultimate_attribute = 500
        self.ultimate_available = 1

        self.start_time = time()
        self.allowed_time = 2 * 60  # 2 minutes allowed time for the player
        self.elapsed_time = 0
        self.restart = False

        self.inventory = []

        self.current_room = Room(25, 25, 0, self.level)
        self.rooms_cleared = 0
        self.current_pos = [0, 0]

        self.character_sprite = get_character_sprite()  # if character sprite is available
        LabelWindow(narrative["spawn"])  # creates a window for the narrative

    def getCurrentPos(self):        # returns the current position of the player
        return self.current_pos

    def getHp(self):                        # GET/SET are self-explanatory
        return self.hp, self.max_hp

    def getGold(self):
        return self.gold

    def getRoomNumber(self):
        return self.rooms_cleared

    def getEnemyPositions(self):
        return self.current_room.enemies.values()

    def getEnemies(self):
        return self.current_room.enemies.items()

    def getEnemy(self, pos):
        for enemy, position in self.current_room.enemies.items():
            if position == pos:     # checks if the character is above the enemy
                return enemy

    def getItem(self, pos):
        for item, position in self.current_room.items.items():
            if position == pos:
                return item

    def getShop(self, pos):
        for shop, position in self.current_room.shops.items():
            if position == pos:
                return shop

    def getItemPositions(self):
        return self.current_room.items.values()

    def getItems(self):
        return self.current_room.items.items()

    def getShops(self):
        return self.current_room.shops

    def getShopPositions(self):
        return self.current_room.shops.values()

    def getXp(self):
        return self.level

    def moveNorth(self):        # moves the character in the specified direction
        self.newPos(-1, 0)

    def moveSouth(self):
        self.newPos(1, 0)

    def moveEast(self):
        self.newPos(0, -1)

    def moveWest(self):
        self.newPos(0, 1)

    def getNextRoom(self):  # This generates the next room when called
        item_count = 25
        enemy_count = 25
        shop_count = 0

        if self.rooms_cleared % 2 == 0:
            shop_count = 100

        self.current_room = Room(item_count, enemy_count, shop_count, self.level)
        self.ultimate_available = 1

    def checkLevel(self):       # checks if the player has leveled up
        if self.to_next_level >= 1:
            self.level += 1
            if self.level == 1:
                LabelWindow(narrative["lvl_up"])
            self.to_next_level = self.to_next_level - 1

    def performAction(self):        # performs the required action (attack/use_item/use_shop/new_room)
        if self.current_pos == self.current_room.matrix[-1]:
            print("Moving to new room...")
            self.rooms_cleared += 1
            self.getNextRoom()
            self.current_pos = self.current_room.matrix[0]

        elif self.current_pos in (eps := self.getEnemyPositions()):
            print("Enemy encountered")
            for pos in eps:
                if pos == self.current_pos:
                    current_enemy = self.getEnemy(pos)
                    self.attackEnemy(current_enemy)
                    break

        elif self.current_pos in (ips := self.getItemPositions()):
            print("Item encountered")
            for pos in ips:
                if pos == self.current_pos:
                    item = self.getItem(pos)
                    self.useItem(item)
                    break

        elif self.current_pos in (sps := self.getShopPositions()):
            print("Shop encountered")
            for pos in sps:
                if pos == self.current_pos:
                    self.useShop()
                    break

    def viewInventory(self):        # instantiates the inventory window
        print("Viewing Inventory")
        invView = InventoryWindow(self)
        invView.viewInventory()
        del invView

    def viewStats(self):            # instantiates the statistics window
        print("Viewing stats")
        statView = StatsWindow(self)
        statView.viewStats()
        del statView

    def attackEnemy(self, enemy):
        if self.enemies_killed == 0:
            LabelWindow(narrative["before_first_kill"])     # narrative window
            self.lvl_2_enemy = True
        elif self.lvl_2_enemy and self.level == 5:
            LabelWindow(narrative["lvl_2_kill"])
            self.lvl_2_enemy = False
            self.lvl_3_enemy = True
        elif self.lvl_3_enemy and self.level > 10:
            LabelWindow(narrative["lvl_3_kill"])
            self.lvl_3_enemy = False

        print("Running attack enemy method")
        enemyAttack = AttackWindow(self, enemy)     # instantiated attack window object
        enemyAttack.startFight()
        if enemyAttack.getResult():     # checks the result of the attack (win/lose/flee)
            if self.enemies_killed == 0:
                LabelWindow(narrative["after_first_kill"])
            self.enemies_killed += 1
            self.current_room.removeEnemy(enemy)
        del enemyAttack     # deletes the AttackWindow object to save memory

    def useItem(self, item):  # This is where the item usage windows are used.
        print("Running use item method")
        itemUse = ItemWindow(self, item)

        if item.name == "Attack" and self.attack_item:      # this is all for narrative
            LabelWindow(narrative["item_attack"])
            self.attack_item = False

        elif item.name == "HP" and self.health_item:
            LabelWindow(narrative["item_health"])
            self.health_item = False

        elif item.name == "Max HP" and self.max_hp_item:
            LabelWindow(narrative["item_max_hp"])
            self.max_hp_item = False

        itemUse.useItem()       # uses the item with collective useItem() method in each class
        if itemUse.getResult():
            try:
                self.current_room.removeItem(item)
            except KeyError:
                self.inventory.remove(item)
        del itemUse

    def useHealthItem(self, val):       # apply the health increase
        if self.hp + val > self.max_hp:
            print("Exceeds max health")
            self.hp = self.max_hp
        else:
            print("Hp increased")
            self.hp += val

    def endGame(self):            # ending the game
        print("Ending game...")
        finalWindow = EndWindow(self)
        finalWindow.viewStatsWrapper()
        if finalWindow.getResult():
            self.restart = True

    def useMaxHealthItem(self, val):        # apply the max_health increase
        print("Max health increased")
        self.max_hp += val
        self.hp += val / 2

    def useAttackItem(self, val):       # apply the attack item
        print("Attack increased")
        self.atk += val

    def storeInInventory(self, item):       # store the item in the inventory
        print("Item stored in inventory")
        self.inventory.append(item)

    def useShop(self):      # instantiates the shop object
        print("Using the shop")
        shopUse = ShopWindow(self)
        shopUse.useShop()

    def newPos(self, x, y):     # checks if the player can move in the chosen direction
        new_x, new_y = self.current_pos
        new_x += x
        new_y += y
        if [new_x, new_y] not in self.current_room.matrix:
            print("Position not possible")  # RETURN AN ERROR FOR THE WINDOW
        else:
            self.current_pos = [new_x, new_y]
