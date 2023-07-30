import presets
import pygameextra as pe
import save_and_load
import display_mesurements as dm
from game_manager import GameManager


class Data:
    surfaces: list
    text: list

    def __init__(self):
        self.measurements = dm.make_measurements()
        self.rects = dm.make_rects(self.measurements)
        self.presets = presets.presets
        self.min_zoom = presets.min_zoom
        self.max_zoom = presets.max_zoom
        self.save = save_and_load.save
        self.ext = save_and_load.ext
        self.state = presets.game_state
        self.game_manager = GameManager(self)

        self.retheme()

    def render_data(self):
        self.render_rects()
        self.render_texts()

    def render_rects(self):
        for rect_dict in self.rects.values():
            for rect in rect_dict.values():
                pe.draw.rect(pe.colors.red, rect, 2)

    def render_texts(self):
        for text in self.text.values():
            if isinstance(text, pe.text.Text):
                pe.draw.rect(pe.colors.green, text.rect, 2)
            elif isinstance(text, list):
                for t in text:
                    pe.draw.rect(pe.colors.green, t.rect, 2)

    def retheme(self):
        self.surfaces, self.text = dm.make_assets(self.ext, self.measurements, self.rects, self.presets, 'Resources/')
