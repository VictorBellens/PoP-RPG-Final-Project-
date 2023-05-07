from graphicInterface.button import Button
from graphicInterface.graphics import *
import random
from common import handle_input, get_exit, log
from datetime import datetime


class AttackWindow:
    def __init__(self, character, enemy):       # handles the attack method
        self.window = GraphWin('Attack', 400, 400)
        self.window.focus_set()
        self.run_flag = True

        self.character = character
        self.enemy = enemy

        self.buttons = [Button(self.window, Point(50, 300), 60, 40, 'Attack', self.__attack, '1'),
                        Button(self.window, Point(150, 300), 60, 40, 'Defend', self.__defend, '2'),
                        Button(self.window, Point(250, 300), 60, 40, 'Ultimate', self.__ultimate, '3'),
                        Button(self.window, Point(350, 300), 60, 40, 'Flee', self.__flee, '4')]
        self.labels = [Text(Point(75, 80), 'You'),
                       Text(Point(325, 80), f'{self.enemy.getName()}')]

        self.enemy_labels = []
        self.character_labels = []
        self.label_count = 1

        self.__setupAll()
        self.__setupSprite()
        self._updateHealth()

    def __setupSprite(self):        # generates the sprites (both enemy and character)
        # makes the image show up in action window
        filename = self.enemy.sprite_action_window
        enemy_png = Image(Point(200, 150), filename)
        enemy_png.draw(self.window)

        # creates rectangle around sprite action window image
        self.sprite_window = Rectangle(Point(150, 100), Point(250, 200))
        self.sprite_window.draw(self.window)

    def __setupAll(self):       # sets up all the required buttons
        for button in self.buttons:
            button.activate()

        for label in self.labels:
            label.draw(self.window)

    def _updateHealth(self):        # basically refreshed the health graphics.
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

    def __attack(self):     # player chose to attack
        chance = random.random()
        if chance > 0.3:
            self.enemy.hp -= self.character.atk
            self._newEnemyLabel(f'-{self.character.atk} HP', 'green')
        else:
            self._newEnemyLabel(f'Missed', 'red')

    def __defend(self):     # player chose to defend
        chance = random.random()
        if chance > 0.2:
            self.character.is_shielded = True
            self._newEnemyLabel(f'Shielded', 'green')
        else:
            self._newEnemyLabel(f'Missed', 'red')

    def __flee(self):       # player chose to flee
        print("Fleeing...")
        self.run_flag = False
        self.window.close()

        return 0

    def __ultimate(self):       # player chose to use ultimate
        if self.character.ultimate_available:
            self._newEnemyLabel(f'Ultimate', 'green')
        else:
            self._newEnemyLabel(f'Unavailable', 'red')

    def _newEnemyLabel(self, label, color):     # creates a new label (attack console) on the right for the enemy
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

    def _newPlayerLabel(self, label, color):    # creates a new label (attack console) on the left for the player
        if self.label_count > 5:
            for labels in self.enemy_labels:
                labels.undraw()
            self.character_labels = []
            self.label_count = 1

        y_pos = (self.label_count * 20) + 90
        text = Text(Point(75, y_pos), label)
        text.setFill(color)
        text.draw(self.window)
        self.enemy_labels.append(text)

    def _winDisplay(self):      # The display when you win, also handles the rewards for winning
        gold_obtained = self.enemy.lvl * 10
        xp_obtained = self.enemy.lvl * 15                # xp level increase here

        self.character.gold += gold_obtained
        self.character.gold_accumulated += gold_obtained
        self.character.to_next_level += xp_obtained/100

        win_text = Text(Point(200, 75), 'Enemy Killed!')
        win_text.draw(self.window)

        gold_text = Text(Point(200, 350), f'Gold obtained: {gold_obtained}')
        gold_text.draw(self.window)

        xp_text = Text(Point(200, 370), f'XP obtained: {xp_obtained}')
        xp_text.draw(self.window)

        get_exit(self)

    def _loseDisplay(self):     # checks if you lost the battle
        lose_text = Text(Point(200, 75), 'You Died!')
        lose_text.draw(self.window)

        get_exit(self)

    def startFight(self):       # main attack loop
        while self.run_flag:
            try:
                self._updateHealth()
            except GraphicsError:   # can't draw the closed window error, if the player closes the window
                break

            if self.enemy.hp <= 0:      # win conditions
                self._winDisplay()
            elif self.character.hp <= 0:
                self._loseDisplay()

            try:
                p, k = handle_input(self.window)        # getting the input event from the user
            except GraphicsError:
                break

            for button in self.buttons:
                if button.clicked(p) or button.pressed(k):      # checks which button was clicked
                    action = button.getAction()
                    res = action()
                    log[datetime.now()] = button.getLabel()[0]      # logs the action
                    if res == 0:
                        break
                    label, color = self.enemy.getResponse(self.character, action)       # gets the response from enemy
                    self._newPlayerLabel(label, color)
                    self.label_count += 1
                    self.enemy.checkIsDead()

    def getResult(self):        # returns True/False if enemy is dead
        return self.enemy.is_dead


class ItemWindow:
    def __init__(self, character, item):        # handles the window for any item
        self.window = GraphWin('Item', 400, 400)
        self.window.focus_set()
        self.run_flag = True

        self.character = character
        self.item = item
        # self.item.sprite_window
        self.item_id = str(item).lower()[7]
        self.item_action = None
        self.__getItemAction(self.item_id)

        self.sprite_window = Rectangle(Point(150, 100), Point(250, 200))
        self.sprite_window.draw(self.window)

        self.buttons = [Button(self.window, Point(150, 300), 60, 40, 'Use', self.item_action, '1'),
                        Button(self.window, Point(250, 300), 60, 40, 'Store', self.character.storeInInventory, '2')]
        self.labels = []

        for button in self.buttons:
            button.activate()

    def __getItemAction(self, item_id):     # sets the proper action depending on the item
        if item_id == 'a':
            self.item_action = self.character.useAttackItem
        elif item_id == 'h':
            self.item_action = self.character.useHealthItem
        elif item_id == 'm':
            self.item_action = self.character.useMaxHealthItem

    def _UseDisplay(self):      # displays the attribute the character gained
        self.run_flag = False
        lose_text = Text(Point(200, 70), f'{self.item.name} increased by {self.item.getAttribute()}!')
        lose_text.draw(self.window)

        get_exit(self)

    def _StoreDisplay(self):        # display for storing the item.
        self.run_flag = False
        self.item.is_selected = True
        lose_text = Text(Point(200, 75), f'{self.item.name} stored in inventory')
        lose_text.draw(self.window)

        get_exit(self)

    def useItem(self):      # main loop for using the item.
        text = Text(Point(200, 250), f'{self.item.name}')
        text.draw(self.window)

        while self.run_flag:
            try:
                p, k = handle_input(self.window)
            except GraphicsError:   # can't draw the closed window error, meaning the user closed the window
                break

            for button in self.buttons:
                if (button.clicked(p) or button.pressed(k)) and button == self.buttons[0]:  # use item
                    action = button.getAction()
                    log[datetime.now()] = button.getLabel()[0]  # logs the action
                    action(self.item.getAttribute())    # performs the action set earlier, and uses the item attribute
                    self._UseDisplay()
                    break
                elif (button.clicked(p) or button.pressed(k)) and button == self.buttons[1]:    # store item
                    action = button.getAction()
                    action(self.item)
                    log[datetime.now()] = button.getLabel()[0]
                    self._StoreDisplay()
                    break

    def getResult(self):        # if the item was used or not.
        return self.item.is_selected


class InventoryWindow:
    def __init__(self, character):      # handles the inventory window
        self.character = character
        x, y = self.__getWindowSize()
        self.window = GraphWin('Inventory', x, y)
        self.window.focus_set()
        self.inventory = self.character.inventory
        self.buttons = []
        self.__createButtons()

    def __getWindowSize(self):      # private method to set the window size accordingly
        if (inv_len := len(self.character.inventory)) < 20:
            return 500, 400
        else:
            return 500, (inv_len/5) * 102

    def __createButtons(self):      # Creates the buttons for each item
        x = 50
        y = 50
        for i, item in enumerate(self.inventory):
            self.buttons.append(Button(self.window, Point(x, y), 100, 100, f'{item.name}', item, None, None))
            if x > 510:
                y += 102
                x = 50
            else:

                x += 102

        for button in self.buttons:
            button.activate()

    def viewInventory(self):        # main loop for viewing the inventory
        p, k, window_closed = None, None, False
        if len(self.character.inventory) == 0:      # nothing in the inventory
            text = Text(Point(250, 200), "There is nothing in your inventory!")
            text.draw(self.window)

        try:
            p, k = handle_input(self.window)
        except GraphicsError:
            window_closed = True

        for button in self.buttons:
            if not window_closed and (p is not None and button.clicked(p)): # checks which item was used
                button.deactivate()
                log[datetime.now()] = button.getLabel()[0]
                item = button.getAction()
                self.character.useItem(item)        # recycles the useItem method from the Character class.

        get_exit(self)


class StatsWindow:
    def __init__(self, character, supered=False):   # handles the stats window
        if not supered:  # checks if the child class has inherited a window from this class.
            self.window = GraphWin('Stats', 400, 400)
            self.window.focus_set()
        self.character = character

    def viewStats(self, to_quit=True):      # main loop for the stats window
        max_hp = self.character.max_hp
        rooms_cleared = self.character.rooms_cleared
        atk = self.character.atk
        enemies_killed = self.character.enemies_killed
        level = self.character.level
        gold_accumulated = self.character.gold_accumulated

        total_xp = int(max_hp/10 * atk * enemies_killed * level * gold_accumulated/10)      # score calculation

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

        if to_quit:
            get_exit(self)


class EndWindow(StatsWindow):
    def __init__(self, character):
        super().__init__(character, supered=True)   # instantiates the stats window object, where only 1 window is made
        self.character = character
        self.window = GraphWin('Stats', 400, 400)
        self.window.focus_set()
        self.result = None

    def viewStatsWrapper(self):     # wraps the viewStats method from StatsWindow
        StatsWindow.viewStats(self, to_quit=False)      # runs the main viewStats method
        play_again = Button(self.window, Point(200, 360), 90, 30, 'Play again', None, 'r')  # create a play_again button
        play_again.activate()
        p, k = None, None

        try:
            p, k = handle_input(self.window)        # get the user input
        except GraphicsError:
            print("Game ended...")

        if (p is not None and play_again.clicked(p)) or play_again.pressed(k):  # checks if play again is clicked
            play_again.deactivate()
            log[datetime.now()] = play_again.getLabel()[0]
            self.result = True
            play_again.activate()

    def getResult(self):        # returns the value of if the player wants to play again
        self.window.close()
        return self.result


class ShopWindow:
    def __init__(self, character):      # handles the shop window
        self.window = GraphWin("Shop", 400, 400)
        self.window.setCoords(0, 0, 4, 4)
        self.window.focus_set()

        self.character = character
        self.runFlag = True

        self.buttons = [Button(self.window, Point(1, 3), 1.5, 0.6, "25% HP Recovery (50 gold)",
                               self.buyHpRecovery25, '1'),
                        Button(self.window, Point(1, 2.25), 1.5, 0.6, "50% HP Recovery (100 gold)",
                               self.buyHpRecovery50, '2'),
                        Button(self.window, Point(1, 1.5), 1.5, 0.6, "100% HP Recovery (200 gold)",
                               self.buyHpRecovery100, '3'),
                        Button(self.window, Point(3, 3), 1.5, 0.6, "Attack Boost +10 (100 gold)",
                               self.buyAttackBoost10, '4'),
                        Button(self.window, Point(3, 2.25), 1.5, 0.6, "Ultimate Power Boost (1000 gold)",
                               self.buyUltimatePowerBoost1000, '5'),
                        Button(self.window, Point(3, 1.5), 1.5, 0.6, "Leave", self.leaveShop, '6')
                        ]   # the buttons for the shop window

        for button in self.buttons:
            button.activate()

    def useShop(self):      # main loop for the shop window
        while self.runFlag:
            p, k = handle_input(self.window)

            for button in self.buttons:
                if button.clicked(p) or button.pressed(k):
                    action = button.getAction()
                    action()
                    log[datetime.now()] = button.getLabel()[0]

    def buyHpRecovery25(self):      # all the below are the options for what the user can buy
        if self.buyHpRecovery(0.25, 50):
            self.displayMessage("25% health recovery purchased")

    def buyHpRecovery50(self):
        if self.buyHpRecovery(0.5, 100):
            self.displayMessage("50% health recovery purchased")

    def buyHpRecovery100(self):
        if self.buyHpRecovery(1, 200):
            self.displayMessage("100% health recovery purchased")

    def buyAttackBoost10(self):
        if self.buyAttackBoost(10, 100):
            self.displayMessage("Attack Boost +10 purchased")

    def buyUltimatePowerBoost1000(self):
        if self.buyUltimatePowerBoost(1000):
            self.displayMessage("Ultimate Power Boost purchased")

    def leaveShop(self):
        self.runFlag = False
        self.window.close()

    def buyHpRecovery(self, percentage, cost):
        if self.character.gold >= cost:
            self.character.gold -= cost
            hpToRecover = int(self.character.max_hp * percentage)
            self.character.hp = min(self.character.hp + hpToRecover, self.character.max_hp)
            return True
        else:
            self.displayMessage("Not enough gold.")
            return False

    def buyAttackBoost(self, boost, cost):
        if self.character.gold >= cost:
            self.character.gold -= cost
            self.character.atk += boost
            return True
        else:
            self.displayMessage("Not enough gold.")
            return False

    def buyUltimatePowerBoost(self, cost):
        if self.character.gold >= cost and self.character.ultimate_available < 2:
            self.character.gold -= cost
            self.character.ultimate_available += 1
            return True
        elif self.character.ultimate_available >= 2:
            self.displayMessage("Maximum ultimate powers reached.")
        else:
            self.displayMessage("Not enough gold.")
        return False

    def displayMessage(self, message):      # displays what has been bought
        message_text = Text(Point(2, 0.75), message)
        message_text.setSize(12)
        message_text.setStyle("bold")
        message_text.setTextColor("red")
        message_text.draw(self.window)
        self.window.getMouse()
        message_text.undraw()


class LabelWindow:
    def __init__(self, message_text):       # this handles most of the narrative prompts
        self.label = message_text
        self.window_size = self.__getWindowSize()
        self.window = GraphWin("Narrative", self.window_size[0], self.window_size[1])
        self.window.focus_set()

        self.text = Text(Point(self.window_size[0]/2, self.window_size[1]/2), self.label)
        self.text.setSize(12)
        self.text.setStyle("bold")
        self.text.draw(self.window)

        get_exit(self)      # get_exit in the constructor because an object of this class is not saved or used again.

    def __getWindowSize(self):  # sets the window size accordingly
        text_size = len(self.label)
        if text_size < 150:
            return 400, 200
        elif text_size < 300:
            return 500, 200
        else:
            return 600, 300
