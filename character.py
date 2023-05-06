from room import Room
from actionWindows import *
from time import time

from common import narrative, get_character_sprite


class Character:    # This is responsible for the character attributes, and all methods tied to room, items, enemy, etc.
    def __init__(self):
        self.max_hp = 100
        self.hp = self.max_hp
        self.atk = 10
        # self.name = None          # 0 implementation
        self.gold = 100

        self.gold_accumulated = 0
        self.enemies_killed = 0
        self.level = 1
        self.to_next_level = 0/100
        self.is_shielded = False

        self.health_item, self.max_hp_item, self.attack_item = True, True, True     # for the narrative
        self.lvl_2_enemy, self.lvl_3_enemy = False, False

        self.ultimate_attribute = 500
        self.ultimate_available = 1

        self.start_time = time()
        self.allowed_time = 2 * 60  # 2 minutes
        self.elapsed_time = 0
        self.restart = False

        self.inventory = []

        self.current_room = Room(25, 25, 0, self.level)
        self.rooms_cleared = 0          # Create a new list attribute which contains all the previous rooms?
        self.current_pos = [0, 0]

        self.character_sprite = get_character_sprite()  # CHARACTER IMAGE HERE
        LabelWindow(narrative["spawn"])

    def getCurrentPos(self):
        return self.current_pos

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

    def getEnemy(self, pos):
        for enemy, position in self.current_room.enemies.items():
            if position == pos:
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

    def moveNorth(self):
        self.newPos(-1, 0)

    def moveSouth(self):
        self.newPos(1, 0)

    def moveEast(self):
        self.newPos(0, -1)

    def moveWest(self):
        self.newPos(0, 1)

    def getNextRoom(self):      # rng will be in #room.py, the var below are only for XP level/difficulty
        item_count = 25
        enemy_count = 25
        shop_count = 0

        if self.rooms_cleared % 2 == 0:
            shop_count = 100

        self.current_room = Room(item_count, enemy_count, shop_count, self.level)
        self.ultimate_available = 1

    def checkLevel(self):
        if self.to_next_level >= 1:
            self.level += 1
            if self.level == 1:
                LabelWindow(narrative["lvl_up"])
            self.to_next_level = self.to_next_level - 1

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

    def viewInventory(self):
        print("Viewing Inventory")
        invView = InventoryWindow(self)
        invView.viewInventory()
        del invView

    def viewStats(self):
        print("Viewing stats")
        statView = StatsWindow(self)
        statView.viewStats()
        del statView

    def attackEnemy(self, enemy):           # here is where we need to implement the attack functions.
        if self.enemies_killed == 0:
            LabelWindow(narrative["before_first_kill"])
            self.lvl_2_enemy = True
        elif self.lvl_2_enemy and self.level == 5:
            LabelWindow(narrative["lvl_2_kill"])
            self.lvl_2_enemy = False
            self.lvl_3_enemy = True
        elif self.lvl_3_enemy and self.level > 10:
            LabelWindow(narrative["lvl_3_kill"])
            self.lvl_3_enemy = False

        print("Running attack enemy method")
        enemyAttack = AttackWindow(self, enemy)
        enemyAttack.startFight()
        if enemyAttack.getResult():
            if self.enemies_killed == 0:
                LabelWindow(narrative["after_first_kill"])
            self.enemies_killed += 1
            self.current_room.removeEnemy(enemy)
        del enemyAttack

    def useItem(self, item):                # here is where we need to implement the shop functions
        print("Running use item method")
        itemUse = ItemWindow(self, item)

        if item.name == "Attack" and self.attack_item:
            LabelWindow(narrative["item_attack"])
            self.attack_item = False

        elif item.name == "HP" and self.health_item:
            LabelWindow(narrative["item_health"])
            self.health_item = False

        elif item.name == "Max HP" and self.max_hp_item:
            LabelWindow(narrative["item_max_hp"])
            self.max_hp_item = False

        itemUse.useItem()
        if itemUse.getResult():
            try:
                self.current_room.removeItem(item)
            except KeyError:
                self.inventory.remove(item)
        del itemUse

    def useHealthItem(self, val):
        if self.hp + val > self.max_hp:
            print("Exceeds max health")
            self.hp = self.max_hp
        else:
            print("Hp increased")
            self.hp += val

    def endGame(self):
        print("Ending game...")
        finalWindow = EndWindow(self)
        finalWindow.viewStatsWrapper()
        if finalWindow.getResult():
            self.restart = True

    def useMaxHealthItem(self, val):
        print("Max health increased")
        self.max_hp += val
        self.hp += val/2

    def useAttackItem(self, val):
        print("Attack increased")
        self.atk += val

    def storeInInventory(self, item):
        print("Item stored in inventory")
        self.inventory.append(item)

    def useShop(self):
        print("Using the shop")
        shopUse = ShopWindow(self)
        shopUse.useShop()

    def newPos(self, x, y):
        new_x, new_y = self.current_pos
        new_x += x
        new_y += y
        if [new_x, new_y] not in self.current_room.matrix:
            print("Position not possible")  # RETURN AN ERROR FOR THE WINDOW
        else:
            self.current_pos = [new_x, new_y]
