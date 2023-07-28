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


def rawColoring(image: pe.Image, color):
    surface = image.surface
    surfaceSize = surface.size
    for y in range(surfaceSize[1]):
        for x in range(surfaceSize[0]):
            if surface.surface.get_at((x, y)) == (0, 0, 0, 255):
                surface.surface.set_at((x, y), color)
    image.surface = surface
    return image


def get_start_game_rects(measurements):
    width = measurements['play_button_width']
    height = measurements['play_button_height']
    return (*GamemodeManager.get_rect(
        measurements,
        measurements['x_center'],
        measurements['play_button_main'],
        width, height), *GamemodeManager.get_rect(
        measurements,
        measurements['x_center'],
        measurements['play_button_resume'],
        width, height))


def make_assets(ext, measurements, presets, resource_folder):
    block_size = [measurements['block_size']] * 2
    font = os.path.join(resource_folder, 'font.ttf')
    start_game_rect, gamemodes_rect, start_game_over_rect, gamemodes_over_rect = get_start_game_rects(measurements)
    height = gamemodes_rect.height
    left_gamemode_rect = pe.rect.Rect(0, 0, *block_size)
    right_gamemode_rect = left_gamemode_rect.copy()
    left_gamemode_over_rect = left_gamemode_rect.copy()
    right_gamemode_over_rect = right_gamemode_rect.copy()
    left_gamemode_rect.center = gamemodes_rect.midleft
    right_gamemode_rect.center = gamemodes_rect.midright
    left_gamemode_over_rect.center = gamemodes_over_rect.midleft
    right_gamemode_over_rect.center = gamemodes_over_rect.midright
    left_gamemode_rect.x += measurements['outline_width_double']
    left_gamemode_over_rect.x += measurements['outline_width_double']
    right_gamemode_rect.x -= measurements['outline_width_double']
    right_gamemode_over_rect.x -= measurements['outline_width_double']
    title_mine_rect = pe.rect.Rect(0, 0, start_game_rect.width * .8, start_game_rect.width * .8)
    title_mine_rect.center = (measurements['x_center'], measurements['y_center_three_fourths'])

    surfaces = {
        'mine': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            title_mine_rect.size, title_mine_rect.topleft
        ), ext['color']),
        'arrowLeft': rawColoring(pe.Image(
            os.path.join(resource_folder, 'arrowLeft.png'),
            block_size, left_gamemode_rect.topleft
        ), ext['text']),
        'arrowRight': rawColoring(pe.Image(
            os.path.join(resource_folder, 'arrowRight.png'),
            block_size, right_gamemode_rect.topleft
        ), ext['text']),
        'arrowLeftSelected': rawColoring(pe.Image(
            os.path.join(resource_folder, 'arrowLeftSelected.png'),
            block_size, left_gamemode_rect.topleft
        ), ext['text']),
        'arrowRightSelected': rawColoring(pe.Image(
            os.path.join(resource_folder, 'arrowRightSelected.png'),
            block_size, right_gamemode_rect.topleft
        ), ext['text']),
        'flagged': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            (20, 20)
        ), ext['background']),
        'flagBackground': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['background']),
        'mineBackground': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['background']),
        'flagText': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['text']),
        'mineText': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['text']),
        'flagColor': rawColoring(pe.Image(
            os.path.join(resource_folder, 'flagged.png'),
            block_size
        ), ext['color']),
        'mineColor': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            block_size
        ), ext['color']),
        'themesText': rawColoring(pe.Image(
            os.path.join(resource_folder, 'themes.png'),
            block_size
        ), ext['text']),
        'themesBackground': rawColoring(pe.Image(
            os.path.join(resource_folder, 'themes.png'),
            block_size
        ), ext['background']),
        'bombed': rawColoring(pe.Image(
            os.path.join(resource_folder, 'mine.png'),
            (20, 20)
        ), ext['background'])
    }
    text = {
        'startGameText': pe.text.Text(START_GAME_TEXT, font, 20, start_game_rect.center, [ext['text'], None]),
        'startGameTextSelected': pe.text.Text(START_GAME_TEXT, font, 20, start_game_rect.center,
                                              [ext['background'], None]),
        'startGameTextOver': pe.text.Text(START_GAME_TEXT, font, 20, start_game_over_rect.center,
                                          [ext['text'], None]),
        'startGameTextSelectedOver': pe.text.Text(START_GAME_TEXT, font, 20, start_game_over_rect.center,
                                                  [ext['background'], None]),
        'beginGameText': pe.text.Text("Tap to begin.", font, 20, (measurements['x_center'], measurements['y_center']),
                                      [ext['background'], None]),
        'gamemodeText': [
            pe.text.Text(gamemode['name'], font, 20, gamemodes_rect.center, [ext['text'], None]) for gamemode in
            presets['gamemodes']
        ]
    }
    return surfaces, text
