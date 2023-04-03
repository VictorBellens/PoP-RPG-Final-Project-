class HealthItem:
    def __init__(self, level):
        self.name = 'HP'
        self.health_added = 10 * level
        self.is_selected = False

    def getAttribute(self):
        self.is_selected = True
        return self.health_added


class MaxHealthItem:
    def __init__(self, level):
        self.name = 'Max HP'
        self.max_health_added = 10 * level
        self.is_selected = False

    def getAttribute(self):
        self.is_selected = True
        return self.max_health_added


class AttackItem:
    def __init__(self, level):
        self.name = 'Attack'
        self.attack_added = 5 * level
        self.is_selected = False

    def getAttribute(self):
        self.is_selected = True
        return self.attack_added


class Barrier:
    def __init__(self):     # This will contain the attributes of a barrier and the usage method.
        pass


class Shop:
    def __init__(self, xp_level):   # This will contain the methods needed for generating/using the shops
        self.player_xp_level = xp_level

    def __setupShopItems(self):
        pass

    def useShop(self):
        return 1
