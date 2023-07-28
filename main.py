from pygameextra.debug import FreeMode

import display_mesurements as dm
import pygameextra as pe
from Data import Data
from menu import MenuManager, touch_button

data = Data()
menu_manager = MenuManager(data)
pe.settings.debugger = FreeMode()
dm.make_display()
do_debug = False


def events(event):
    global do_debug
    pe.event.quitCheckAuto()
    pe.mouse.fingersupport.handle_finger_events(False)
    if pe.event.key_DOWN(pe.pygame.K_ESCAPE):
        do_debug = True


while True:
    [events(event) for event in pe.event.get()]

    if pe.settings.recording:
        pe.stop_recording()
    pe.start_recording()

    pe.fill.full(data.ext['background'])
    if data.state == 'menu':
        menu_manager.main_menu()
    elif data.state == 'pregame':
        data.game_manager.render_animation()
    elif data.state == 'startgame':
        data.game_manager.render_animation(True)
        if pe.mouse.clicked()[0]:
            data.game_manager.begin_game()

    pe.display.update()

    if len(pe.mouse.fingersupport.fingers) == 0:
        touch_button.buttons.clear()

    if do_debug:
        pe.stop_recording()
        pe.start_debug()
        do_debug = False
