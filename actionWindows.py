from graphicInterface.button import Button
from graphicInterface.graphics import *


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

        player_health = Rectangle(Point(145, 200), Point(150, p_health_converted))
        player_health.setFill('green')
        enemy_health = Rectangle(Point(255, e_health_converted), Point(250, 200))
        enemy_health.setFill('red')

        player_health.draw(self.window)
        enemy_health.draw(self.window)

    def __attack(self):
        pass

    def __defend(self):
        pass

    def __flee(self):
        print("Fleeing...")
        self.run_flag = False
        self.window.close()

    def __ultimate(self):
        pass

    def _updateLabels(self):
        pass

    def _playerLabels(self):
        pass

    def _enemyLabels(self):
        pass

    def _winDisplay(self):
        win_text = Text(Point(200, 75), 'Enemy Killed!')
        win_text.draw(self.window)
        p = self.window.getMouse()

        if 0 <= p.getX() <= 400 and 0 <= p.getY() <= 400:
            self.run_flag = False
            self.window.close()

    def _loseDisplay(self):
        pass

    def startFight(self):
        while self.run_flag:
            self._updateHealth()
            if self.enemy.hp <= 0:
                self.character.gold += 10
                self._winDisplay()

            try:
                p = self.window.getMouse()
            except GraphicsError:
                break

            for button in self.buttons:
                if button.clicked(p):
                    action = button.getAction()
                    action()
                    self.enemy.getResponse(self.character, action)

    def getResult(self):
        return self.enemy.is_dead


class InventoryWindow:
    def __init__(self):
        self.window = None
        self.buttons = [Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None),
                        Button(self.window, Point(665, 500), 60, 40, '', None)]


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
