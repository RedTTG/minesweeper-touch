from menu.gamemode_manager import GamemodeManager
from menu.theme_manager import ThemeManager


class MenuManager:
    def __init__(self, data):
        self.data = data
        self.theme_manager = ThemeManager(data)
        self.gamemode_manager = GamemodeManager(data)

    def main_menu(self):
        # self.theme_manager.render()
        self.gamemode_manager.render(
            self.data.measurements['x_center'],
            self.data.measurements['play_button_main'],
        )

    def retheme(self):  # TODO: add re-theming
        self.theme_manager.retheme()
        self.gamemode_manager.retheme()
