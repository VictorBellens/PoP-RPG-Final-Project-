from graphicInterface.button import Button
from graphicInterface.graphics import *
import random


class AttackWindow:
    def __init__(self, character, enemy):
        self.window = GraphWin('Attack', 400, 400)
        self.run_flag = True

        self.character = character
        self.enemy = enemy

        self.sprite_window = Rectangle(Point(150, 100), Point(250, 200))
        self.sprite_window.draw(self.window)

        self.buttons = [Button(self.window, Point(50, 300), 60, 40, 'Attack', self.__attack),
                        Button(self.window, Point(150, 300), 60, 40, 'Defend', self.__defend),
                        Button(self.window, Point(250, 300), 60, 40, 'Ultimate', self.__ultimate),
                        Button(self.window, Point(350, 300), 60, 40, 'Flee', self.__flee)]
        self.labels = [Text(Point(75, 80), 'You'),
                       Text(Point(325, 80), f'{self.enemy.getName()}')]

        self.enemy_labels = []
        self.player_labels = []
        self.label_count = 1

        self.__setupAll()
        self._updateHealth()

    def __setupAll(self):
        for button in self.buttons:
            button.activate()

        for label in self.labels:
            label.draw(self.window)

    def _updateHealth(self):
        p_max_health = Rectangle(Point(145, 200), Point(150, 100))
        p_max_health.setFill('grey')
        e_max_health = Rectangle(Point(250, 200), Point(255, 100))
        e_max_health.setFill('grey')

        p_max_health.draw(self.window)
        e_max_health.draw(self.window)

        p_health_converted = 200 - (self.character.hp / self.character.max_hp) * 100
        e_health_converted = 200 - (self.enemy.hp / self.enemy.max_hp) * 100

        if e_health_converted >= 200:
            e_health_converted = 200

        if p_health_converted >= 200:
            p_health_converted = 200

        player_health = Rectangle(Point(145, 200), Point(150, p_health_converted))
        player_health.setFill('green')
        enemy_health = Rectangle(Point(255, e_health_converted), Point(250, 200))
        enemy_health.setFill('red')

        player_health.draw(self.window)
        enemy_health.draw(self.window)

    def __attack(self):
        chance = random.random()
        if chance > 0.3:
            self.enemy.hp -= self.character.atk
            self._newEnemyLabel(f'-{self.character.atk} HP', 'green')
        else:
            self._newEnemyLabel(f'Missed', 'red')

    def __defend(self):
        chance = random.random()
        if chance > 0.3:
            self.character.is_shielded = True
            self._newEnemyLabel(f'Shielded', 'green')
        else:
            self._newEnemyLabel(f'Missed', 'red')

    def __flee(self):
        print("Fleeing...")
        self.run_flag = False
        self.window.close()

        return 0

    def __ultimate(self):
        if self.character.ultimate_available:
            self._newEnemyLabel(f'Ultimate', 'green')
        else:
            self._newEnemyLabel(f'Unavailable', 'red')

    def _newEnemyLabel(self, label, color):
        if self.label_count > 5:
            for labels in self.enemy_labels:
                labels.undraw()
            self.enemy_labels = []
            self.label_count = 1

        y_pos = (self.label_count * 20) + 90
        text = Text(Point(325, y_pos), label)
        text.setFill(color)
        text.draw(self.window)
        self.enemy_labels.append(text)

    def _newPlayerLabel(self, label, color):
        if self.label_count > 5:
            for labels in self.enemy_labels:
                labels.undraw()
            self.player_labels = []
            self.label_count = 1

        y_pos = (self.label_count * 20) + 90
        text = Text(Point(75, y_pos), label)
        text.setFill(color)
        text.draw(self.window)
        self.enemy_labels.append(text)

    def _updateLabels(self):
        pass

    def _playerLabels(self):
        pass

    def _enemyLabels(self):
        pass

    def _winDisplay(self):
        gold_obtained = self.enemy.lvl * 10
        xp_obtained = self.enemy.lvl * 10

        self.character.gold += gold_obtained
        self.character.gold_accumulated += gold_obtained
        self.character.to_next_level += xp_obtained/100

        win_text = Text(Point(200, 75), 'Enemy Killed!')
        win_text.draw(self.window)

        gold_text = Text(Point(200, 350), f'Gold obtained: {gold_obtained}')
        gold_text.draw(self.window)

        xp_text = Text(Point(200, 370), f'XP obtained: {xp_obtained}')
        xp_text.draw(self.window)

        p = self.window.getMouse()
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.run_flag = False
            self.window.close()

    def _loseDisplay(self):
        lose_text = Text(Point(200, 75), 'You Died!')
        lose_text.draw(self.window)

        p = self.window.getMouse()
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.run_flag = False
            self.window.close()

    def startFight(self):
        while self.run_flag:
            self._updateHealth()

            if self.enemy.hp <= 0:
                self._winDisplay()

            elif self.character.hp <= 0:
                self._loseDisplay()

            try:
                p = self.window.getMouse()
            except GraphicsError:
                break

            for button in self.buttons:
                if button.clicked(p):
                    action = button.getAction()
                    res = action()
                    if res == 0:
                        break
                    label, color = self.enemy.getResponse(self.character, action)
                    self._newPlayerLabel(label, color)
                    self.label_count += 1
                    self.enemy.checkIsDead()

    def getResult(self):
        return self.enemy.is_dead


class ItemWindow:
    def __init__(self, character, item):
        self.window = GraphWin('Item', 400, 400)
        self.run_flag = True

        self.character = character
        self.item = item
        self.item_id = str(item).lower()[7]
        self.item_action = None
        self.__getItemAction(self.item_id)

        self.sprite_window = Rectangle(Point(150, 100), Point(250, 200))
        self.sprite_window.draw(self.window)

        self.buttons = [Button(self.window, Point(150, 300), 60, 40, 'Use', self.item_action),
                        Button(self.window, Point(250, 300), 60, 40, 'Store', self.character.storeInInventory)]
        self.labels = []

        for button in self.buttons:
            button.activate()

    def __getItemAction(self, item_id):
        if item_id == 'a':
            self.item_action = self.character.useAttackItem
        elif item_id == 'h':
            self.item_action = self.character.useHealthItem
        elif item_id == 'm':
            self.item_action = self.character.useMaxHealthItem

    def _UseDisplay(self):
        self.run_flag = False
        lose_text = Text(Point(200, 70), f'{self.item.name} increased by {self.item.getAttribute()}!')
        lose_text.draw(self.window)

        p = self.window.getMouse()
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.run_flag = False
            self.window.close()

    def _StoreDisplay(self):
        self.run_flag = False
        self.item.is_selected = True
        lose_text = Text(Point(200, 75), f'{self.item.name} stored in inventory')
        lose_text.draw(self.window)

        p = self.window.getMouse()
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.run_flag = False
            self.window.close()

    def useItem(self):
        text = Text(Point(200, 250), f'{self.item.name}')
        text.draw(self.window)

        while self.run_flag:
            try:
                p = self.window.getMouse()
            except GraphicsError:
                break

            for button in self.buttons:
                if button.clicked(p) and button == self.buttons[0]:
                    action = button.getAction()
                    action(self.item.getAttribute())
                    self._UseDisplay()
                    break
                elif button.clicked(p) and button == self.buttons[1]:
                    action = button.getAction()
                    action(self.item)
                    self._StoreDisplay()
                    break
            break

    def getResult(self):
        return self.item.is_selected


class InventoryWindow:
    def __init__(self, character):
        self.window = GraphWin('Inventory', 400, 400)
        self.character = character
        self.buttons = []

    def viewInventory(self):
        temp = Text(Point(200, 200), 'This is where we view the inventory (temp)')
        temp.draw(self.window)
        temp1 = Text(Point(200, 215), f'{self.character.inventory}')
        temp1.draw(self.window)

        try:
            p = self.window.getMouse()
        except GraphicsError:
            self.window.close()
            return
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.window.close()


class SettingsWindow:
    def __init__(self):
        self.window = None
        self.buttons = [Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None)]


class ShopWindow:
    def __init__(self):
        self.window = None
        self.buttons = [Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None)]


class StatsWindow:
    def __init__(self, character):
        self.window = GraphWin('Stats', 400, 400)
        self.character = character

    def viewStats(self):
        max_hp = self.character.max_hp
        rooms_cleared = self.character.rooms_cleared
        atk = self.character.atk
        enemies_killed = self.character.enemies_killed
        level = self.character.level
        gold_accumulated = self.character.gold_accumulated

        total_xp = int(max_hp/10 * atk * enemies_killed * level * gold_accumulated/10)

        max_hp_label = Text(Point(200, 100), f'Max HP: {max_hp}')
        rooms_cleared_label = Text(Point(200, 125), f'Rooms cleared: {rooms_cleared}')
        atk_label = Text(Point(200, 150), f'Attack attribute: {atk}')
        enemies_killed_label = Text(Point(200, 175), f'Enemies killed: {enemies_killed}')
        level_label = Text(Point(200, 200), f'Level: {level}')
        gold_accumulated_label = Text(Point(200, 225), f'Accumulated gold: {gold_accumulated}')
        total_xp_label = Text(Point(200, 300), f'Score: {total_xp}')

        labels = [max_hp_label, rooms_cleared_label, level_label, atk_label,
                  enemies_killed_label, total_xp_label, gold_accumulated_label]
        for label in labels:
            label.draw(self.window)

        try:
            p = self.window.getMouse()
        except GraphicsError:
            self.window.close()
            return
        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.window.close()
