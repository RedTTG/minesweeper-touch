import pygameextra as pe

pe.init((0, 0))
SCREEN_SIZE, SCREEN_MODE = (0, 0), 2  # Screen size
TITLE_TEXT = "Minesweeper touch"


def make_display():
    global SCREEN_SIZE
    pe.display.make(SCREEN_SIZE, TITLE_TEXT, SCREEN_MODE)


def make_measurements():
    global SCREEN_SIZE
    SCREEN_SIZE = pe.display.get_size()
    measurements = {
        'outline_width': (SCREEN_SIZE[0] / SCREEN_SIZE[1]) * 2,
        'x_center': SCREEN_SIZE[0] * .5,
        'y_center': SCREEN_SIZE[1] * .5,
        'play_button_main': SCREEN_SIZE[1] * .65,
        'play_button_resume': SCREEN_SIZE[0] * .75,
        'play_button_width': SCREEN_SIZE[0] * .15,
        'play_button_height': SCREEN_SIZE[1] * .05,
    }
    double = {f'{key}_double': int(value * 2) for key, value in measurements.items()}
    half = {f'{key}_half': int(value * .5) for key, value in measurements.items()}
    four_thirds = {f'{key}_four_thirds': int(value * 1.25) for key, value in measurements.items()}
    three_fourths = {f'{key}_three_fourths': int(value * .75) for key, value in measurements.items()}
    quarter = {f'{key}_quarter': int(value * .25) for key, value in measurements.items()}
    final_measurements = {**measurements, **double, **half, **quarter, **three_fourths, **four_thirds}
    return {key: int(value) for key, value in final_measurements.items()}

def make_assets(measurements, ):
    surfaces = {

    }