import random
from items import Item, Shop
from enemy import Enemy, Boss


class Room:     # This is responsible for the room information such as enemy/item/boss/obstruction locations
    def __init__(self, item_count, enemy_count, barrier_count, shop_count, xp_level):
        self.room_id = None
        self.matrix = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                       [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
                       [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7],
                       [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7],
                       [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7],
                       [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7],
                       [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
                       [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]]

        self.items = {Item(): [0, 2]}
        self.enemies = {}
        self.shops = {}
        self.barriers = {}      # could be for door/window/obstruction/bushes/etc.
        self.blocked = [[0, 0], self.matrix[-1]]    # blocks where items/enemies CANNOT be placed

        self.__setDifficulty(xp_level)
        self.__setItemCount(item_count)
        self.__setEnemyCount(enemy_count)
        self.__setBarrierCount(barrier_count)
        self.__setShopCount(shop_count, xp_level)   # we need setBarriers so that two objects cannot be on the same spot

    def __setDifficulty(self, xp_level):
        pass

    def __setItemCount(self, item_chance):
        pass

    def __setEnemyCount(self, enemy_chance):
        # while True:
        #     enemies = round(enemy_chance/10 * random.random())    # program hangs: takes too long to find value > 1
        #
        #     if enemies > 1:     # change when difficulty level is implemented
        #         break
        enemies = round(enemy_chance / 10) * random.randint(1, 3)

        for n in range(enemies):
            self.enemies[Enemy()] = self.locationGenerator()

    def __setBarrierCount(self, barrier_chance):
        pass

    def __setShopCount(self, shop_chance, xp_level):
        if shop_chance == 100:
            self.shops[Shop(xp_level)] = self.locationGenerator()   # Shop() is non-functional

    def locationGenerator(self):
        max_x = int(len(self.matrix)/8)
        max_y = int(len(self.matrix)/8)

        x, y = 0, 0
        while [x, y] in self.blocked:
            x = random.randint(0, max_x - 1)
            y = random.randint(0, max_y - 1)
        return [x, y]

    def getStartingPos(self):
        return self.matrix[0]
