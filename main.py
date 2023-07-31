from pygameextra.debug import FreeMode

import display_mesurements as dm
import pygameextra as pe
from Data import Data
from menu import MenuManager, touch_button

data = Data()
# Changeable constants
data.DEBUG = True

# Init
menu_manager = MenuManager(data)
pe.settings.debugger = FreeMode()
dm.make_display()
do_debug = False


def events(event):
    global do_debug
    pe.event.quitCheckAuto()
    pe.mouse.fingersupport.handle_finger_events(False)
    if data.DEBUG:
        if pe.event.key_DOWN(pe.pygame.K_RETURN):
            do_debug = True
    if pe.event.key_DOWN(pe.pygame.K_ESCAPE):
        data.state = 'menu'


while True:
    [events(event) for event in pe.event.get()]

    if data.DEBUG:
        if pe.settings.recording:
            pe.stop_recording()
        pe.start_recording()

    pe.fill.full(data.ext['background'])

    if data.state == 'menu':
        # Main menu
        menu_manager.main()
    elif data.state == 'pregame':
        # Bubble animation
        data.game_manager.render_animation()
    elif data.state == 'start_game':
        # Start game text
        data.game_manager.render_animation(True)
        if pe.mouse.clicked()[0]:
            # Generate board and zoom in to game
            data.game_manager.begin_game()
    elif data.state == 'in_game':
        data.game_manager.render_game()

    if data.DEBUG:
        data.render_data()

    pe.display.update()

    if len(pe.mouse.fingersupport.fingers) == 0:
        touch_button.buttons.clear()

    if data.DEBUG and do_debug:
        pe.stop_recording()
        pe.start_debug()
        do_debug = False
