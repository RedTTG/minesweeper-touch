from presets import presets
from pickle import dump, load

ext = {}


def save():
    global ext
    with open('save.mst', 'wb') as save_file:
        dump(ext, save_file)


try:
    with open('save.mst', 'rb') as save_load:
        ext = load(save_load)
except FileNotFoundError:
    ext = {
        **presets['themes'][0],
        'gamemode': 0
    }
    save()
