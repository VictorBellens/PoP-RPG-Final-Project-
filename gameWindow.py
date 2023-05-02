from graphicInterface.graphics import *
from graphicInterface.button import Button

from character import Character
from common import handle_input, log, get_player_profile

from datetime import datetime
from time import time, ctime


class GameWindow:   # This controls the UI and button functionality
    def __init__(self, save_log, change_profile=False):
        self.rooms = []
        self.character = Character()

        self.run_flag = True
        self.save_log = save_log
        self.change_profile = change_profile
        self.start_time = time()

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

        if not change_profile:
            self._instantiateGraphicMethods()

    def _instantiateGraphicMethods(self):
        self.window = GraphWin('RPG', 600, 600)  # Window set to 600x600
        self.__drawControlButtons()
        self.__drawRoomGrid()
        self.window.update()
        self.window.focus_set()

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

        time_text = Text(Point(100, 480), f'{ctime(self.character.elapsed_time)[14:20]} '
                                          f'/ {int(self.character.allowed_time/60)}:00')

        self.labels = [hp_text, hp_rect, gold_text, xp_rect, xp_text, time_text]

        for label in self.labels:
            label.draw(self.window)

    def _updatePlayerLocation(self):  # can add smoother graphics here if we want (see #animation.py)
        x, y = self.character.getCurrentPos()

        self.player_position.undraw()
        self.player_position = Image(self.display_matrix[x][y], self.character.character_sprite)
        self.player_position.draw(self.window)

    def _updateEnemyLocation(self):                         # It is likely that we can replace all the updatesItem/Enemy
        enemies = list(self.character.getEnemies())
        print(enemies)

        for pos in self.enemy_positions:
            pos.undraw()

        for enemy, enemy_pos in enemies:
            x, y = enemy_pos
            filename = enemy.sprite_window
            enemy_png = Image(self.display_matrix[x][y], filename)
            enemy_png.draw(self.window)
            self.enemy_positions.append(enemy_png)

    def _updateItemLocation(self):
        items = list(self.character.getItems())

        for pos in self.item_positions:
            pos.undraw()

        for item, item_pos in items:
            x, y = item_pos
            print(item_pos, item)

            filename = item.sprite_map
            item_png = Image(self.display_matrix[x][y], filename)
            item_png.draw(self.window)
            self.item_positions.append(item_png)

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

    def _updateTimer(self):
        self.character.elapsed_time = (time() - self.character.start_time) - (15 * self.character.enemies_killed)
        if self.character.elapsed_time < 0:
            self.character.elapsed_time = 0
        if self.character.elapsed_time > self.character.allowed_time:
            self.window.close()
            self.character.endGame()

    def startWindow(self):
        if self.change_profile:
            get_player_profile("player_sprite 50x50.png")   # change to correct directory
            self._instantiateGraphicMethods()

        while self.run_flag:
            try:
                self._updateTimer()
                self._updateLabels()
                self._updatePlayerLocation()
                self._updateEnemyLocation()
                self._updateItemLocation()
                self._updateShopLocation()
            except GraphicsError:       # can't draw to closed window error, meaning the user closed the window
                print("Game ended...")
                break

            if self.character.hp <= 0:          # NEEDS MORE WORK
                self.window.close()
                self.character.endGame()
                if self.character.restart:
                    print("Restarting game...")
                    new_game = GameWindow(save_log=True)
                    new_game.startWindow()
                else:
                    self.run_flag = False

            try:
                p, k = handle_input(self.window)
            except GraphicsError:
                print("Game ended...")
                self.character.endGame()
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

        if self.character.restart:
            print("Restarting game...")
            new_game = GameWindow(save_log=True)
            new_game.startWindow()

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
