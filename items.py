class HealthItem:
    def __init__(self, level):
        self.name = 'HP'
        self.health_added = 10 * level
        self.is_selected = False
        self.sprite_map = 'health&attackItems/Health_item55x55.png'
        self.sprite_window = None

    def getAttribute(self):
        self.is_selected = True
        return self.health_added


class MaxHealthItem:
    def __init__(self, level):
        self.name = 'Max HP'
        self.max_health_added = 10 * level
        self.is_selected = False
        self.sprite_map = 'health&attackItems/max_health_item_55x55.png'
        self.sprite_window = None

    def getAttribute(self):
        self.is_selected = True
        return self.max_health_added


class AttackItem:
    def __init__(self, level):
        self.name = 'Attack'
        self.attack_added = 5 * level
        self.is_selected = False
        self.level = level  # This is the level of the character, NOT the enemy (comes from character.py)
        self.sprite_map = self.__getMapImage()
        self.sprite_window = self.__getWindowImage()

    def __getMapImage(self):  # takes the enemy level, finds the image corresponding enemy level, then returns the image
        filename = None

        if self.level < 5:
            filename = 'spriteMap/Green Monster 55x55.png'
        elif 5 <= self.level < 10:
            filename = 'spriteMap/PurpleMonst2 55x55.png'
        elif self.level > 10:
            filename = 'spriteMap/Red Monster 55x55.png'

        return filename

    def __getWindowImage(self):
        filename = None

        if self.level < 5:
            filename = 'spriteActionWindow/Green Monster 148x148.png'
        elif 5 <= self.level < 10:
            filename = 'spriteActionWindow/PurpleMonst2 148x148.png'
        elif self.level > 10:
            filename = 'spriteActionWindow/Red Monster 148x148.png'

        return filename

    def getAttribute(self):
        self.is_selected = True
        return self.attack_added


class Shop:
    def __init__(self, xp_level):   # This will contain the methods needed for generating/using the shops
        self.player_xp_level = xp_level
        self.sprite_map = 'health&attackItems/Health_item55x55.png'  # CHANGE THIS AFTER BOZO
        self.sprite_window = None
