import display_mesurements as dm
import pygameextra as pe
from Data import Data
from menu import MenuManager

data = Data()
menu_manager = MenuManager(data)

dm.make_display()

while True:
    [pe.event.quitCheckAuto() for event in pe.event.get()]
    pe.fill.full(data.ext['background'])
    menu_manager.main_menu()
    pe.display.update()
