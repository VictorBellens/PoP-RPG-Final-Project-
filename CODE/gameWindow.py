from graphicInterface.graphics import *
from graphicInterface.button import Button

from character import Character
from common import handle_input, log

from datetime import datetime

from PIL import Image, ImageTk
from graphics import *

class GameWindow:   # This controls the UI and button functionality
    def __init__(self, save_log):
        self.window = GraphWin('RPG', 600, 600)     # Window set to 600x600
        self.rooms = []
        self.character = Character()

        self.run_flag = True
        self.save_log = save_log

        # positions of items
        self.enemy_positions = []
        self.item_positions = []
        self.shop_positions = []
        self.barrier_positions = []
        self.player_position = Circle(Point(0, 0), 0)      # Instantiated player position circle object

        # action block buttons
        self.attack_buttons = []
        self.pickup_buttons = []
        self.shop_buttons = []
        self.inventory_buttons = []
        self.labels = []
        self.control_buttons = []

        self.__drawControlButtons()
        self.__drawRoomGrid()

    def __drawRoomGrid(self):
        margin_x = 50
        margin_y = 50
        grid_width = 500
        grid_height = 350
        num_rows = 8
        num_columns = 8

        cell_width = grid_width / num_columns
        cell_height = grid_height / num_rows

        self.display_matrix = []

        for i in range(num_rows):
            row = []
            for j in range(num_columns):
                top_left = Point(margin_x + j * cell_width, margin_y + i * cell_height)
                bottom_right = Point(margin_x + (j + 1) * cell_width, margin_y + (i + 1) * cell_height)
                center_x = (top_left.getX() + bottom_right.getX()) / 2
                center_y = (top_left.getY() + bottom_right.getY()) / 2
                center = Point(center_x, center_y)
                row.append(center)
                cell = Rectangle(top_left, bottom_right)
                cell.draw(self.window)

                if i == 0 and j == 0:
                    cell.setFill(color_rgb(191, 224, 224))

                elif i == num_rows-1 and j == num_columns-1:
                    cell.setFill(color_rgb(191, 224, 224))

            self.display_matrix.append(row)

    def __drawControlButtons(self):
        Rectangle(Point(50, 50), Point(550, 400)).draw(self.window)  # where the game matrix will be displayed
        sc = self.character

        self.control_buttons.append(Button(self.window, Point(300, 450), 40, 40, '↑', sc.moveNorth, 'Up'))
        self.control_buttons.append(Button(self.window, Point(300, 530), 40, 40, '↓', sc.moveSouth, 'Down'))
        self.control_buttons.append(Button(self.window, Point(260, 490), 40, 40, '←', sc.moveEast, 'Left'))
        self.control_buttons.append(Button(self.window, Point(340, 490), 40, 40, '→', sc.moveWest, 'Right'))

        self.control_buttons.append(Button(self.window, Point(440, 450), 70, 40, 'action', sc.performAction, 'space'))
        self.control_buttons.append(Button(self.window, Point(440, 490), 70, 40, 'inventory', sc.viewInventory, 'i'))
        self.control_buttons.append(Button(self.window, Point(440, 530), 70, 40, 'stats', sc.viewStats, 's'))   # tbc

        self.control_buttons.append(Button(self.window, Point(75, 530), 40, 40, 'quit', self.quit, 'q'))    # quit game

        for button in self.control_buttons:
            button.activate()

    def _updateLabels(self):
        self.character.checkLevel()
        for label in self.labels:
            label.undraw()

        hp, max_hp = self.character.getHp()
        level = self.character.level
        gold = self.character.getGold()
        hp_converted = ((hp/max_hp) * 90) + 90
        xp_converted = 100 + (self.character.to_next_level * 400)

        hp_text = Text(Point(65, 420), 'HP')

        max_hp_rect = Rectangle(Point(90, 410), Point(180, 430))
        max_hp_rect.setFill(color_rgb(226, 226, 226))
        max_hp_rect.draw(self.window)

        hp_rect = Rectangle(Point(90, 410), Point(hp_converted, 430))
        hp_rect.setFill(color_rgb(140, 255, 167))

        xp_max_rect = Rectangle(Point(100, 40), Point(500, 45))
        xp_max_rect.setFill(color_rgb(223, 223, 223))
        xp_max_rect.draw(self.window)

        xp_rect = Rectangle(Point(100, 40), Point(xp_converted, 45))
        xp_rect.setFill('green')

        xp_text = Text(Point(300, 30), f'{level}')

        gold_text = Text(Point(86, 450), f'Gold: {gold}')

        self.labels = [hp_text, hp_rect, gold_text, xp_rect, xp_text]

        for label in self.labels:
            label.draw(self.window)

    def _updatePlayerLocation(self):  # can add smoother graphics here if we want (see #animation.py)
        x, y = self.character.getCurrentPos()
        self.player_position.undraw()
        self.player_position = Image(self.display_matrix[x][y], "spriteMap/Player 55x55.png")
        self.player_position.draw(self.window)


    def _updateEnemyLocation(self):                         # It is likely that we can replace all the updatesItem/Enemy
        enemies_positions = self.character.getEnemyPositions()
        enemies = self.character.getEnemies()
        for pos in self.enemy_positions:
            pos.undraw()

        for enemy_pos, enemy in zip(enemies_positions, enemies):
            x, y = enemy_pos
            image = Image(self.display_matrix[x][y], "spriteMap/Green Monster 55x55.png")
            image.draw(self.window)
            self.enemy_positions.append(image)


    def _updateItemLocation(self):
        items = self.character.getItemPositions()
        for pos in self.item_positions:
            pos.undraw()

        for item_pos in items:
            x, y = item_pos
            position = Circle(self.display_matrix[x][y], 12)
            position.setFill(color_rgb(70, 70, 160))
            position.draw(self.window)
            self.item_positions.append(position)

    def _updateShopLocation(self):
        shops = self.character.getShopPositions()
        for pos in self.shop_positions:
            pos.undraw()

        for shop_pos in shops:
            x, y = shop_pos
            position = Circle(self.display_matrix[x][y], 12)
            position.setFill(color_rgb(230, 230, 0))
            position.draw(self.window)
            self.shop_positions.append(position)

    def _updateBarrierLocation(self):
        pass

    def startWindow(self):
        while self.run_flag:
            self._updateLabels()
            self._updatePlayerLocation()
            self._updateEnemyLocation()
            self._updateItemLocation()
            self._updateShopLocation()

            if self.character.hp <= 0:          # NEEDS MORE WORK
                self.window.close()
                self.character.viewStats()

            try:
                p, k = handle_input(self.window)
            except GraphicsError:
                print("Game ended...")
                break

            for button in self.control_buttons:
                if (p is not None and button.clicked(p)) or button.pressed(k):
                    button.deactivate()
                    log[datetime.now()] = button.getLabel()[0]
                    action = button.getAction()
                    action()
                    button.activate()

                    self.window.update()
                    self.window.focus_set()

    def quit(self):
        if self.save_log:
            with open('logFile.txt', 'w', encoding='utf-8') as logfile:
                logfile.write(f'Log from {str(datetime.now())[:11]}\nTotal actions: {len(log)}\n')
                logfile.write(f'Start time: {str(list(log.keys())[0])[11:19]}\n'
                              f'End time:   {str(list(log.keys())[-1])[11:19]}')
                logfile.write(f'\n\n  Time   | Action\n')
                for t, n in log.items():
                    logfile.write(f'{str(t)[11:19]} | {n}\n')
            print("Log saved to logFile.txt successfully")
        self.run_flag = False
