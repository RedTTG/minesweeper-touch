import presets
import save_and_load
import display_mesurements as dm
from game_manager import GameManager


class Data:
    surfaces: list
    text: list

    def __init__(self):
        self.measurements = dm.make_measurements()
        self.presets = presets.presets
        self.min_zoom = presets.min_zoom
        self.max_zoom = presets.max_zoom
        self.save = save_and_load.save
        self.ext = save_and_load.ext
        self.state = presets.game_state
        self.game_manager = GameManager(self)

        self.retheme()

    def retheme(self):
        self.surfaces, self.text = dm.make_assets(self.ext, self.measurements, self.presets, 'Resources/')
