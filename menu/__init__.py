from menu.gamemode_manager import GamemodeManager
from menu.theme_manager import ThemeManager


class MenuManager:
    def __init__(self, data):
        self.data = data
        self.theme_manager = ThemeManager(data)
        self.gamemode_manager = GamemodeManager(data)

    def main(self):
        # self.theme_manager.render()
        self.data.surfaces['title_mine'].display()
        self.gamemode_manager.render()

    def over(self):
        self.gamemode_manager.render('_over')

    def retheme(self):  # TODO: add re-theming
        self.theme_manager.retheme()
        self.gamemode_manager.retheme()
