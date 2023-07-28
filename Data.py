import presets
import save_and_load
import display_mesurements as dm


class Data:
    def __init__(self):
        self.measurements = dm.make_measurements()
        self.assets = dm.make_assets(self.measurements, 'Resources/')
        self.presets = presets.presets
        self.min_zoom = presets.min_zoom
        self.max_zoom = presets.max_zoom
        self.save = save_and_load.save
        self.ext = save_and_load.ext
        self.state = presets.game_state
