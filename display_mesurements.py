import pygameextra as pe
import os

from menu import GamemodeManager

pe.init((0, 0))
SCREEN_SIZE, SCREEN_MODE = (0, 0), 2  # Screen size
TITLE_TEXT = "Minesweeper touch"

START_GAME_TEXT = "New Game"


def make_display():
    global SCREEN_SIZE
    pe.display.make(SCREEN_SIZE, TITLE_TEXT, SCREEN_MODE)


def make_measurements():
    global SCREEN_SIZE
    SCREEN_SIZE = pe.display.get_size()
    measurements = {
        'screen_width': SCREEN_SIZE[0],
        'screen_height': SCREEN_SIZE[1],
        'outline_width': (SCREEN_SIZE[0] / SCREEN_SIZE[1]) * 2,
        'x_center': SCREEN_SIZE[0] * .5,
        'y_center': SCREEN_SIZE[1] * .5,
        'play_button_main': SCREEN_SIZE[1] * .65,
        'play_button_resume': SCREEN_SIZE[0] * .75,
        'play_button_width': SCREEN_SIZE[0] * .15,
        'play_button_height': SCREEN_SIZE[1] * .05,
        'block_size': (SCREEN_SIZE[0] / SCREEN_SIZE[1]) * 20,
    }
    double = {f'{key}_double': int(value * 2) for key, value in measurements.items()}
    half = {f'{key}_half': int(value * .5) for key, value in measurements.items()}
    four_thirds = {f'{key}_four_thirds': int(value * 1.25) for key, value in measurements.items()}
    three_fourths = {f'{key}_three_fourths': int(value * .75) for key, value in measurements.items()}
    quarter = {f'{key}_quarter': int(value * .25) for key, value in measurements.items()}

    final_measurements = {**measurements, **double, **half, **quarter, **three_fourths, **four_thirds}
    pre_final_measurements = {key: int(value) for key, value in final_measurements.items()}
    pre_final_measurements['screen'] = SCREEN_SIZE
    pre_final_measurements['screen_rect'] = pe.rect.Rect(0, 0, *SCREEN_SIZE)
    pre_final_measurements['screen_half'] = [int(value * .5) for value in pre_final_measurements['screen']]
    return pre_final_measurements


def make_rects(measurements):
        width = measurements['play_button_width']
        height = measurements['play_button_height']
        start_game_rect, gamemodes_rect, left_gamemode_rect, right_gamemode_rect  = GamemodeManager.get_rect(
            measurements,
            measurements['x_center'],
            measurements['play_button_main'],
            width, height)
        start_game_over_rect, gamemodes_over_rect, left_gamemode_over_rect, right_gamemode_over_rect = GamemodeManager.get_rect(
            measurements,
            measurements['play_button_resume'],
            measurements['y_center'],
            width, height)

        rects = {
            'start_game': {
                'rect': start_game_rect,
            },
            'start_game_over': {
                'rect': start_game_over_rect,
            },
            'gamemode': {
                'rect': gamemodes_rect,
                'left': left_gamemode_rect,
                'right': right_gamemode_rect,
            },
            'gamemode_over': {
                'rect': gamemodes_over_rect,
                'left': left_gamemode_over_rect,
                'right': right_gamemode_over_rect,
            },
            'title_mine': {
                'rect': pe.rect.Rect(0, 0, start_game_rect.width * .8, start_game_rect.width * .8),
            }
        }
        rects['title_mine']['rect'].center = (measurements['x_center'], measurements['y_center_three_fourths'])
        return rects


def rawColoring(image: pe.Image, color):
    surface = image.surface
    surfaceSize = surface.size
    for y in range(surfaceSize[1]):
        for x in range(surfaceSize[0]):
            if surface.surface.get_at((x, y)) == (0, 0, 0, 255):
                surface.surface.set_at((x, y), color)
    image.surface = surface
    return image


def make_assets(ext, measurements, rects, presets, resource_folder):
    block_size = [measurements['block_size']] * 2
    font = os.path.join(resource_folder, 'font.ttf')



    surfaces = {
        'title_mine': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            rects['title_mine']['rect'].size, rects['title_mine']['rect'].topleft
        ), ext['color']),
        'flagged': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            (20, 20)
        ), ext['background']),
        'flag_background': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['background']),
        'mine_background': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['background']),
        'flag_text': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['text']),
        'mineText': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['text']),
        'flag_color': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['color']),
        'mine_color': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['color']),
        'themes_text': rawColoring(pe.Image(
            os.path.join(resource_folder, 'themes.png'),
            block_size
        ), ext['text']),
        'themes_ackground': rawColoring(pe.Image(
            os.path.join(resource_folder, 'themes.png'),
            block_size
        ), ext['background']),
        'bombed': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            (20, 20)
        ), ext['background'])
    }

    for side in ['left', 'right']:
        for selected in ['', '_selected']:
            for over in ['', '_over']:
                surfaces[f'{side}_gamemode{selected}{over}'] = rawColoring(pe.Image(
                    os.path.join(resource_folder, f'{side}_gamemode{selected}.png'),
                    rects[f'gamemode{over}'][side].size, rects[f'gamemode{over}'][side].topleft
                ), ext['text'])

    text = {
        'beginGameText': pe.text.Text("Tap to begin.", font, 20, (measurements['x_center'], measurements['y_center']),
                                      [ext['background'], ext['color']]),
    }
    for selected in ['', '_selected']:
        for over in ['', '_over']:
            text[f'start_game{selected}{over}'] = pe.text.Text(START_GAME_TEXT, font, 20,
                                                               rects[f'start_game{over}']['rect'].center,
                                                               [ext['background'] if selected else ext['text'], None])
    for over in ['', '_over']:
        text[f'gamemode{over}'] = [
            pe.text.Text(gamemode['name'], font, 20, rects[f'gamemode{over}']['rect'].center, [ext['text'], None]) for gamemode
            in
            presets['gamemodes']
        ]
    return surfaces, text
