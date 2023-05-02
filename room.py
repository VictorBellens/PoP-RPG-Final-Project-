import random
from items import Shop, HealthItem, AttackItem, MaxHealthItem
from enemy import Enemy


class Room:     # This is responsible for the room information such as enemy/item/boss/obstruction locations
    def __init__(self, item_count, enemy_count, shop_count, xp_level):
        self.room_id = None
        self.matrix = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                       [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
                       [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7],
                       [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7],
                       [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7],
                       [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7],
                       [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
                       [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]]

        self.items = {}
        self.enemies = {}
        self.shops = {}
        self.blocked = [self.matrix[0], self.matrix[-1]]    # blocks where items/enemies CANNOT be placed

        self.__setItemCount(item_count, xp_level)
        self.__setEnemyCount(enemy_count, xp_level)
        self.__setShopCount(shop_count, xp_level)

        print(f"\nNumber of items: {len(self.items)}\n"
              f"Number of enemies: {len(self.enemies)}\n"
              f"Number of shops: {len(self.shops)}\n")    # for debug only

    def __setItemCount(self, item_chance, level):
        items = round(item_chance / 10) * random.randint(1, 3)      # create more rng here...

        for n in range(items):
            chance = random.random()
            if chance < 0.33:
                self.items[AttackItem(level)] = self.locationGenerator()
            elif chance < 0.66:
                self.items[HealthItem(level)] = self.locationGenerator()
            elif chance < 1:
                self.items[MaxHealthItem(level)] = self.locationGenerator()

    def __setEnemyCount(self, enemy_chance, level):
        enemies = round(enemy_chance / 10) * random.randint(1, 3)   # create more rng here...

        for n in range(enemies):
            loc = self.locationGenerator()
            self.enemies[Enemy(level, loc)] = loc

    def __setShopCount(self, shop_chance, xp_level):
        if shop_chance == 100:
            self.shops[Shop(xp_level)] = self.locationGenerator()

    def locationGenerator(self):
        max_x = int(len(self.matrix)/8)
        max_y = int(len(self.matrix)/8)

        x, y = 0, 0
        while [x, y] in self.blocked:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)

        self.blocked.append([x, y])
        return [x, y]

    def removeEnemy(self, enemy):
        self.enemies.pop(enemy)

    def removeItem(self, item):
        self.items.pop(item)

    def removeShop(self, shop):
        self.shops.pop(shop)

    def getStartingPos(self):
        return self.matrix[0]
