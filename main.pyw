import random
import cornerFloodAlgorithm as flood
import pygameextra as pe
from pygameextra.fpslogger import Logger

from presets import presets
from save_and_load import save, ext

from pygameextra.debug import FreeMode, Debugger

pe.init()
ss, mode = (1920, 1080), 2  # Screen size
# ss, mode = (1200, 600), 1
# ss, mode = (700, 700), 1
pe.display.make(ss, "Minesweeper touch", mode)  # 2 for fullscreen
# Size Settings
max_zoom = 4
min_zoom = 0.4
rect = (10, 10)

surface = pe.Surface(rect)

# Zoom and pan presets
debug = False  # True to debug zoom and pan
activate_debug = False
zoompoint = (0, 0)
zoom_start_pos = (0, 0)
ss = pe.display.display_reference.size
scalex = 1
scaley = 1
posx = ss[0] / 2 - rect[0] / 2  # center X
posy = ss[1] / 2 - rect[1] / 2  # center Y
fingers = []
zooming = False
moving = False
distance = 0


#
def worldtoscreen(worldx, worldy):
    return worldx * scalex + posx, \
           worldy * scaley + posy


def screentoworld(screenx, screeny):
    return (screenx - posx) / scalex, \
           (screeny - posy) / scaley


# Preset data

# Game data
board = None
boardMap = None
game_state = 'menuInit'
res = {}
pregame_animation = 0
scale_animationX = scalex
scale_animationY = scaley
scale_animationPX = posx
scale_animationPY = posy
scale_animationEnable = True
tapMode = 'flag'
gameJustBegun = True
round_amount = 12
openings = []
buttons = {}
fingers = []
filterClosed = None
filterFlagged = None
animation = []


# Game functions
def generateEmptyBoard(gridX, gridY, isMap=False):
    board = []
    for y in range(gridY):
        layer = []
        for x in range(gridX):
            if isMap:
                layer.append('closed')
            else:
                layer.append('empty')
        board.append(layer)
    return board


def neighbouringSquares(center, gridX, gridY, filter=None, board=None):
    randomX = center[0]
    randomY = center[1]
    area = [
        (randomY + 1, randomX - 1),
        (randomY + 1, randomX),
        (randomY + 1, randomX + 1),
        (randomY, randomX - 1),
        (randomY, randomX + 1),
        (randomY - 1, randomX - 1),
        (randomY - 1, randomX),
        (randomY - 1, randomX + 1)]
    i = 0
    while i < len(area):
        area[i] = (area[i][1], area[i][0])
        if area[i][0] < 0 or area[i][0] > gridX - 1:
            del area[i]
        elif area[i][1] < 0 or area[i][1] > gridY - 1:
            del area[i]
        elif filter is not None and board is not None and board[area[i][1]][area[i][0]] != filter:
            del area[i]
        else:
            i += 1
    return area


def uncover(startX, startY, gridX, gridY):
    global boardMap, board, openings
    visited = []
    unvisited = {(startX, startY)}
    sizeOfOpening = 30
    uncovered = 0
    while unvisited:
        current = unvisited.pop()
        visited.append(current)
        openings.append([current, sizeOfOpening])
        animation.append({
            'type': 'opening',
            'location': current
        })
        uncovered += 1
        sizeOfOpening += 1
        surround = 0
        empty = []
        for neighbour in neighbouringSquares(current, gridX, gridY):
            if neighbour not in visited:
                if board[neighbour[1]][neighbour[0]] == 'bomb':
                    surround += 1
                elif boardMap[neighbour[1]][neighbour[0]] == 'closed':
                    empty.append(neighbour)
        if surround == 0:
            boardMap[current[1]][current[0]] = 'opened'
            unvisited.update(empty)
        else:
            boardMap[current[1]][current[0]] = str(surround)
    return uncovered


def generateBoard(gridX, gridY, bombMin, bombMax, startX, startY):
    global board, boardMap
    ok = False
    while not ok:
        board = generateEmptyBoard(gridX, gridY)
        boardMap = generateEmptyBoard(gridX, gridY, True)
        protected = [
            (startX - 1, startY + 1),
            (startX, startY + 1),
            (startX + 1, startY + 1),
            (startX - 1, startY),
            (startX, startY),
            (startX + 1, startY),
            (startX - 1, startY - 1),
            (startX, startY - 1),
            (startX + 1, startY - 1),
        ]  # Area around start to be protected
        bombs = random.randint(bombMin, bombMax)
        i = 0
        while i < bombs:
            randomX = random.randint(0, gridX - 1)
            randomY = random.randint(0, gridY - 1)
            randomLocation = (randomX, randomY)
            area = [
                board[min(max(randomY + 1, 0), gridY - 1)][min(max(randomX - 1, 0), gridX - 1)],
                board[min(max(randomY + 1, 0), gridY - 1)][randomX],
                board[min(max(randomY + 1, 0), gridY - 1)][min(max(randomX + 1, 0), gridX - 1)],
                board[randomY][min(max(randomX - 1, 0), gridX - 1)],
                board[randomY][min(max(randomX + 1, 0), gridX - 1)],
                board[min(max(randomY - 1, 0), gridY - 1)][min(max(randomX - 1, 0), gridX - 1)],
                board[min(max(randomY - 1, 0), gridY - 1)][randomX],
                board[min(max(randomY - 1, 0), gridY - 1)][min(max(randomX + 1, 0), gridX - 1)],
            ]
            if (randomLocation in protected) or (board[randomY][randomX] == 'bomb') or (not ('empty' in area)):
                continue
            board[randomY][randomX] = 'bomb'
            i += 1
        visited = []
        unvisited = {(startX, startY)}
        while unvisited:
            current = unvisited.pop()
            visited.append(current)
            for neighbour in neighbouringSquares(current, gridX, gridY):
                if board[neighbour[1]][neighbour[0]] == "empty":
                    if neighbour not in visited:
                        unvisited.add(neighbour)
        if len(visited) + bombs == gridX * gridY:
            ok = True
            # Generate map
            uncover(startX, startY, gridX, gridY)
    return board, boardMap


def rawColoring(image: pe.Image, color):
    surface = image.surface
    surfaceSize = surface.size
    for y in range(surfaceSize[1]):
        for x in range(surfaceSize[0]):
            if surface.surface.get_at((x, y)) == (0, 0, 0, 255):
                surface.surface.set_at((x, y), color)
    image.surface = surface
    return image


def reloadData():
    # Images
    res['mine'] = rawColoring(pe.Image('Resources/mine.png', (200, 200)), ext['color'])
    res['arrowLeft'] = rawColoring(pe.Image('Resources/arrowLeft.png', (30, 30)), ext['text'])
    res['arrowRight'] = rawColoring(pe.Image('Resources/arrowRight.png', (30, 30)), ext['text'])
    res['arrowLeftSelected'] = rawColoring(pe.Image('Resources/arrowLeftSelected.png', (30, 30)), ext['text'])
    res['arrowRightSelected'] = rawColoring(pe.Image('Resources/arrowRightSelected.png', (30, 30)), ext['text'])
    res['flagged'] = rawColoring(pe.Image('Resources/flagged.png', (20, 20)), ext['background'])
    res['flagBackground'] = rawColoring(pe.Image('Resources/flagged.png', (30, 30)), ext['background'])
    res['mineBackground'] = rawColoring(pe.Image('Resources/mine.png', (30, 30)), ext['background'])
    res['flagText'] = rawColoring(pe.Image('Resources/flagged.png', (30, 30)), ext['text'])
    res['mineText'] = rawColoring(pe.Image('Resources/mine.png', (30, 30)), ext['text'])
    res['flagColor'] = rawColoring(pe.Image('Resources/flagged.png', (30, 30)), ext['color'])
    res['mineColor'] = rawColoring(pe.Image('Resources/mine.png', (30, 30)), ext['color'])
    res['themesText'] = rawColoring(pe.Image('Resources/themes.png', (30, 30), (ss[0] - 70, 40)), ext['text'])
    res['themesBackground'] = rawColoring(pe.Image('Resources/themes.png', (30, 30), (ss[0] - 70, 40)),
                                          ext['background'])
    res['bombed'] = rawColoring(pe.Image('Resources/mine.png', (20, 20)), ext['background'])
    # Texts
    res['gamemodeText'] = []
    for gamemode in presets['gamemodes']:
        res['gamemodeText'].append(
            pe.text.Text(gamemode['name'], "Resources/font.ttf", 20, (ss[0] / 2, ss[1] / 2 + 65), [ext['text'], None]))
    res['startGameText'] = pe.text.Text("New Game", "Resources/font.ttf", 20, (ss[0] / 2, ss[1] / 2 + 120),
                                        [ext['text'], None])
    res['startGameTextSelected'] = pe.text.Text("New Game", "Resources/font.ttf", 20, (ss[0] / 2, ss[1] / 2 + 120),
                                                [ext['background'], None])
    # Over edition
    res['gamemodeTextOver'] = []
    for gamemode in presets['gamemodes']:
        res['gamemodeTextOver'].append(
            pe.text.Text(gamemode['name'], "Resources/font.ttf", 20, (ss[0] - ss[0] / 6, ss[1] / 2 + 15),
                         [ext['text'], None]))
    res['startGameTextOver'] = pe.text.Text("New Game", "Resources/font.ttf", 20, (ss[0] - ss[0] / 6, ss[1] / 2 + 120),
                                            [ext['text'], None])
    res['startGameTextSelectedOver'] = pe.text.Text("New Game", "Resources/font.ttf", 20,
                                                    (ss[0] - ss[0] / 6, ss[1] / 2 + 120), [ext['background'], None])
    #
    res['beginGameText'] = pe.text.Text("Tap to begin.", "Resources/font.ttf", 20, (ss[0] / 2, ss[1] / 2),
                                        [ext['background'], None])
    res['font'] = pe.pygame.font.Font("Resources/font.ttf", 15)


# Button functions
def leftArrow():
    if ext['gamemode'] > 0:
        ext['gamemode'] -= 1


def rightArrow():
    if ext['gamemode'] < len(presets['gamemodes']) - 1:
        ext['gamemode'] += 1


def startNewGame():
    global game_state, pregame_animation, rect, surface, posx, posy, scalex, scaley
    game_state = 'pregame'
    pregame_animation = 0
    gamemode = ext['gamemode']
    gamemode = presets['gamemodes'][gamemode]
    rect = (30 * gamemode['grid'][0], 30 * gamemode['grid'][1])
    scalex = ((ss[1] - 100) / rect[1])
    scaley = scalex
    posx = ss[0] / 2 - rect[0] * scalex / 2  # center X
    posy = ss[1] / 2 - rect[1] * scaley / 2  # center Y
    surface = pe.Surface(rect)


def tapModeBomb():
    global tapMode
    tapMode = 'bomb'


def tapModeFlag():
    global tapMode
    tapMode = 'flag'


# Custom functions

class touchButton:
    def image(rect, ic, ac, action=None):
        global fingers, buttons
        if not len(fingers) > 0:
            ic.display()
            return
        fingerPosition = list((fingers[0]['pos'][0], fingers[0]['pos'][1]))
        fingerRect = pe.rect.Rect(fingerPosition[0] - 10, fingerPosition[1] - 10, 20, 20)
        buttonRect = pe.rect.Rect(*rect)
        if fingerRect.colliderect(buttonRect) and action is not None:
            ac.display()
            if str(rect) not in buttons:
                action()
                buttons[str(rect)] = True
        elif str(rect) in buttons:
            del buttons[str(rect)]
            ic.display()
        else:
            ic.display()

    def rect(rect, ic, ac, action=None):
        global fingers, buttons
        if not len(fingers) > 0:
            pe.draw.rect(ic, rect, 0)
            return
        fingerPosition = list((fingers[0]['pos'][0], fingers[0]['pos'][1]))
        fingerRect = pe.rect.Rect(fingerPosition[0] - 10, fingerPosition[1] - 10, 20, 20)
        buttonRect = pe.rect.Rect(*rect)
        if fingerRect.colliderect(buttonRect) and action is not None:
            pe.draw.rect(ac, rect, 0)
            if str(rect) not in buttons:
                action()
                buttons[str(rect)] = True
        elif str(rect) in buttons:
            del buttons[str(rect)]
            pe.draw.rect(ic, rect, 0)
        else:
            pe.draw.rect(ic, rect, 0)


#

def drawRound(color, sides, rect):
    pe.draw.rect(color, (rect[0], rect[1], rect[2], rect[3]), 0,
                 edge_rounding_top_left=round_amount if sides[0] else -1,
                 edge_rounding_top_right=round_amount if sides[1] else -1,
                 edge_rounding_bottom_left=round_amount if sides[2] else -1,
                 edge_rounding_bottom_right=round_amount if sides[3] else -1)


# Initialize
reloadData()
# pe.settings.debugger = FreeMode()
# pe.settings.debugger = Debugger()
log = Logger()
lastpos = (posx, posy)
lastSelect = (-1, -1)
lastfinger = (0, 0)
fingerRect = pe.rect.Rect(-10, -10, 10, 10)
pressMove = False
noZoomBefore = True
loc2 = (rect[0] + 100, rect[1] + 100)
themesMenu = False
themesMenu2 = False
changeThemeIndex = 0


def changeTheme():
    global game_state
    theme = presets['themes'][changeThemeIndex]
    ext['background'] = theme['background']
    ext['color'] = theme['color']
    ext['text'] = theme['text']
    save()
    reloadData()
    game_state = 'menuInit'


def toggleThemeMenu():
    global themesMenu, themesMenu2
    themesMenu = not themesMenu
    themesMenu2 = True


def themeMenu():
    global changeThemeIndex
    pe.draw.circle(ext['text'], pe.math.center((40, 40, 30, 30)), 32, 0)
    pe.draw.circle(ext['background'], pe.math.center((40, 40, 30, 30)), 30, 0)
    pe.draw.rect(ext['text'], (55, 23, ss[0] - 110, 64), 0)
    pe.draw.rect(ext['background'], (55, 25, ss[0] - 110, 60), 0)
    x, y = pe.math.center((40, 40, 30, 30))
    i = 0
    while i < len(presets['themes']):
        if not (ext['color'] == presets['themes'][i]['color'] and ext['background'] == presets['themes'][i][
            'background']):
            changeThemeIndex = i
            touchButton.rect((x - 18, y - 18, 36, 36), ext['background'], presets['themes'][i]['background'],
                             changeTheme)
            pe.draw.circle(presets['themes'][i]['background'], (x, y), 18, 0)
            pe.draw.circle(presets['themes'][i]['color'], (x, y), 10, 0)
        else:
            pe.draw.circle(ext['text'], (x, y), 23, 0)
            pe.draw.circle(ext['color'], (x, y), 22, 0)
            pe.draw.circle(ext['background'], (x, y), 15, 0)
        x += (ss[0] - 110) / len(presets['themes'])
        i += 1


#
if __name__ == "__main__":
    run = True
else:
    run = False
#

while run:
    # Handle zoom and pan
    for pe.event.c in pe.event.get():
        pe.event.quitCheckAuto()
        size = pe.display.get_size()
        if pe.event.c.type == pe.pygame.FINGERDOWN:
            fingers.append({
                'id': pe.event.c.finger_id,
                'pos': (pe.event.c.x * size[0], pe.event.c.y * size[1])
            })
        elif pe.event.c.type == pe.pygame.FINGERMOTION:
            i = 0
            while i < len(fingers):
                if fingers[i]['id'] == pe.event.c.finger_id:
                    fingers[i]['pos'] = (pe.event.c.x * size[0], pe.event.c.y * size[1])
                    break
                i += 1
        elif pe.event.c.type == pe.pygame.FINGERUP:
            i = 0
            while i < len(fingers):
                if fingers[i]['id'] == pe.event.c.finger_id:
                    del fingers[i]
                    break
                i += 1
        elif pe.event.key_DOWN(pe.pygame.K_ESCAPE):
            game_state = "menuInit"
        elif pe.event.key_DOWN(pe.pygame.K_RETURN):
            activate_debug = True
        else:
            i = 0
            while i < len(fingers):
                if fingers[i]['id'] == "mouse":
                    del fingers[i]
                    break
                i += 1
        # if pe.mouse.clicked()[0]:
        #     fingers.append({
        #         'id': "mouse",
        #         'pos': pe.mouse.pos()
        #     })

    if pe.settings.recording:
        pe.stop_recording()
    pe.start_recording()
    pe.fill.full(ext['background'])
    if 'game' in game_state and len(fingers) == 2 and not zooming:
        distance = pe.math.dist(fingers[0]['pos'], fingers[1]['pos'])
        zoom_start_pos = pe.math.lerp_legacy(
            fingers[0]['pos'],
            fingers[1]['pos'],
            distance / 2
        )
        start_scalex = scalex
        start_scaley = scaley
        original = tuple(zoom_start_pos)
        zoom_start_pos = screentoworld(*zoom_start_pos)
        zooming = True
        scale_animationEnable = False
        moving = False
    elif 'game' in game_state and len(fingers) == 2 and zooming:
        distance_new = pe.math.dist(fingers[0]['pos'], fingers[1]['pos'])
        change = distance_new - distance
        change *= 0.02
        scalex = min(max(start_scalex * 1 + change, min_zoom), max_zoom)
        scaley = min(max(start_scaley * 1 + change, min_zoom), max_zoom)
        zoompoint = pe.math.lerp_legacy(
            fingers[0]['pos'],
            fingers[1]['pos'],
            distance_new / 2
        )
        afterzoomx, afterzoomy = screentoworld(*original)
        # print((zoom_start_pos[0] - afterzoomx), (zoom_start_pos[1] - afterzoomy))
        dist = pe.math.dist(zoom_start_pos, (afterzoomx, afterzoomy))
        diffx, diffy = (zoom_start_pos[0] - afterzoomx), (zoom_start_pos[1] - afterzoomy)
        posx -= diffx * scalex
        posy -= diffy * scaley
        original = tuple(zoompoint)
        zoom_start_pos = screentoworld(*zoompoint)
        scale_animationEnable = False
    elif 'game' in game_state and len(fingers) == 1 and not moving and not zooming:
        distance = fingers[0]['pos']
        firstdistance = fingers[0]['pos']
        lastfinger = fingers[0]['pos']
        moving = True
        scale_animationEnable = False
    elif 'game' in game_state and len(fingers) == 1 and moving and not zooming:
        lastfinger = fingers[0]['pos']
        posx += (fingers[0]['pos'][0] - distance[0])  # * 1.5
        posy += (fingers[0]['pos'][1] - distance[1])  # * 1.5
        distance = fingers[0]['pos']
        if not gameJustBegun:
            scale_animationEnable = False
    elif len(fingers) == 1:
        zooming = False
        moving = True
        distance = fingers[0]['pos']
        firstdistance = fingers[0]['pos']
        lastfinger = fingers[0]['pos']
        noZoomBefore = False
    elif moving and noZoomBefore:
        change = (lastfinger[0] - firstdistance[0]) + (lastfinger[1] - firstdistance[1])
        if abs(change) < 0.1:
            pressMove = True
        else:
            pressMove = False
        moving = False
    elif moving:
        pressMove = False
        moving = False
    else:
        moving = False
        pressMove = False
        lastfinger = None
        gameJustBegun = False
        noZoomBefore = True

    if game_state == 'ingame' or game_state == 'pregameover' or game_state == 'gameover':
        if scale_animationEnable and scale_animationX > scalex and scale_animationY > scaley:
            change = 0.02
            scalex = min(max(scalex * 1 + change, min_zoom), max_zoom)
            scaley = min(max(scaley * 1 + change, min_zoom), max_zoom)
            afterzoomx, afterzoomy = screentoworld(scale_animationPX, scale_animationPY)

            dist = pe.math.dist(loc, (afterzoomx, afterzoomy))
            diffx, diffy = (loc[0] - afterzoomx), (loc[1] - afterzoomy)
            posx -= diffx * scalex
            posy -= diffy * scaley
            original = (scale_animationPX, scale_animationPY)
            loc = screentoworld(scale_animationPX, scale_animationPY)
        else:
            scale_animationEnable = False
        screenRect = (
            0, 0,
            ss[0],
            ss[1]
        )
        gameRect = (
            posx, posy,
            rect[0] * scalex + posx,
            rect[1] * scaley + posy
        )
        visibleRect = (
            max(screenRect[0], min(screenRect[2], gameRect[0])),
            max(screenRect[1], min(screenRect[3], gameRect[1])),
            max(screenRect[0], min(screenRect[2], gameRect[2])),
            max(screenRect[1], min(screenRect[3], gameRect[3]))
        )
        visibleRect = (*screentoworld(visibleRect[0], visibleRect[1]), *screentoworld(visibleRect[2], visibleRect[3]))
        visibleRect = pe.rect.Rect(visibleRect[0], visibleRect[1], visibleRect[2] - visibleRect[0],
                                   visibleRect[3] - visibleRect[1])
        temp = pe.display.display_reference
        pe.display.context(surface)
        # Inner display

        pe.fill.full(ext['background'])
        for y in range(len(board)):
            for x in range(len(board[y])):
                if not pe.rect.Rect(x * 30, y * 30, 30, 30).colliderect(visibleRect):
                    continue
                if board[y][x] == 'bomb' and 'gameover' in game_state:
                    # pe.draw.rect(ext['background'], (x * 30, y * 30, 30, 30), 0)
                    if (x, y) == lastSelect:
                        drawRound(ext['color'], filterClosed[y][x], (x * 30, y * 30, 30, 30))
                        drawRound(pe.colors.red, [True, True, True, True], (x * 30, y * 30, 30, 30))
                    elif boardMap[y][x] == 'flagged':
                        drawRound((97, 98, 80), filterFlagged[y][x], (x * 30, y * 30, 30, 30))
                    else:
                        drawRound(ext['color'], filterClosed[y][x], (x * 30, y * 30, 30, 30))
                    pe.display.blit(res['bombed'].surface, (x * 30 + 5, y * 30 + 5))
                elif boardMap[y][x] == 'closed':
                    # pe.draw.rect(ext['background'], (x*30, y*30, 30, 30), 0)
                    drawRound(ext['color'], filterClosed[y][x], (x * 30, y * 30, 30, 30))
                elif boardMap[y][x] == 'flagged':
                    # pe.draw.rect(ext['background'], (x * 30, y * 30, 30, 30), 0)
                    drawRound((97, 98, 80), filterFlagged[y][x], (x * 30, y * 30, 30, 30))
                    pe.display.blit(res['flagged'].surface, (x * 30 + 5, y * 30 + 5))
                elif boardMap[y][x] != 'opened' and scalex > 0.7 and scaley > 0.7:
                    # pe.draw.rect(ext['background'], (x * 30, y * 30, 30, 30), 0)
                    centerOfText = pe.math.center((x * 30, y * 30, 30, 30))
                    text = res['font'].render(boardMap[y][x], True, ext['text'])
                    textRect = text.get_rect()
                    textRect.center = centerOfText
                    pe.display.blit(text, textRect)
                    if scalex <= 1 and scaley <= 1:
                        b = ext['background']
                        pe.draw.rect((b[0], b[1], b[2], 255 * scalex / 2), (x * 30, y * 30, 30, 30), 0)
                else:
                    pe.draw.rect(ext['background'], (x * 30, y * 30, 30, 30), 0)
                if boardMap[y][x] in 'opened12345678' and scalex > 0.7 and scaley > 0.7:
                    c = ext['color']
                    gamemodeGrid = presets['gamemodes'][ext['gamemode']]['grid']
                    if boardMap[min(max(y - 1, 0), gamemodeGrid[1])][
                        min(max(x, 0), gamemodeGrid[0])] in 'opened12345678':
                        pe.draw.line((c[0], c[1], c[2], 200), (x * 30 + 7.5, y * 30), (x * 30 + 22.5, y * 30), 1)
                    if boardMap[min(max(y, 0), gamemodeGrid[1])][
                        min(max(x - 1, 0), gamemodeGrid[0])] in 'opened12345678':
                        pe.draw.line((c[0], c[1], c[2], 200), (x * 30, y * 30 + 7.5), (x * 30, y * 30 + 22.5), 1)
                    if scalex <= 1 and scaley <= 1:
                        b = ext['background']
                        pe.draw.rect((b[0], b[1], b[2], 255 * scalex / 2), (x * 30, y * 30, 30, 30), 0)
        i = 0
        while i < len(openings):
            sizeOfOpening = min(30, openings[i][1])
            locationOfOpening = (
            openings[i][0][0] * 30 + (30 - sizeOfOpening) / 2, openings[i][0][1] * 30 + (30 - sizeOfOpening) / 2)
            rectOpening = (*locationOfOpening, *[sizeOfOpening] * 2)
            if pe.rect.Rect(*rectOpening).colliderect(visibleRect):
                drawRound(ext['color'], [True] * 4, (*locationOfOpening, *[sizeOfOpening] * 2))
            openings[i][1] -= 2
            if openings[i][1] <= 5:
                del openings[i]
            else:
                i += 1

        if len(fingers) > 0:
            loc2 = screentoworld(*fingers[0]['pos'])
            fingerPosition = fingers[0]['pos']
            fingerRect = pe.rect.Rect(fingerPosition[0] - 10, fingerPosition[1] - 10, 20, 20)
        elif not pressMove:
            loc2 = (rect[0] + 100, rect[1] + 100)
        uiRect = pe.rect.Rect(ss[0] / 2 - 60, ss[1] - ss[1] / 10 - 31, 120, 62)
        if 'gameover' not in game_state and (not fingerRect.colliderect(uiRect)) and ((not moving) or pressMove) and (
        not zooming) and loc2[0] <= rect[0] and loc2[1] <= rect[1]:
            lastpos = (posx, posy)
            gridX = int(loc2[0] / 30)
            gridY = int(loc2[1] / 30)
            lastSelect = (gridX, gridY)
            if boardMap[gridY][gridX] == 'closed':
                if tapMode == 'flag':
                    boardMap[gridY][gridX] = 'flagged'
                    filterClosed = flood.filtered(boardMap, 'closed')
                    filterFlagged = flood.filtered(boardMap, 'flagged')
                    animation.append({
                        'type': 'flagged',
                        'location': (gridX, gridY)
                    })
                elif board[gridY][gridX] == 'bomb':
                    game_state = 'pregameover'
                else:
                    uncovered = uncover(gridX, gridY, *presets['gamemodes'][ext['gamemode']]['grid'])
                    filterClosed = flood.filtered(boardMap, 'closed')
                    filterFlagged = flood.filtered(boardMap, 'flagged')
            elif tapMode == 'flag' and boardMap[gridY][gridX] == 'flagged':
                boardMap[gridY][gridX] = 'closed'
                gamemode = presets['gamemodes'][ext['gamemode']]
                filterClosed = flood.filtered(boardMap, 'closed')
                filterFlagged = flood.filtered(boardMap, 'flagged')
                animation.append({
                    'type': 'closed',
                    'location': (gridX, gridY)
                })
        pressMove = False

        # End of inner display
        if debug:
            pe.draw.circle(pe.colors.black, screentoworld(*pe.mouse.pos()), 10, 0)
        surface = pe.display.display_reference
        pe.display.context(temp)
        # Draw the inner display

        tempSurface = pe.Surface((visibleRect[2], visibleRect[3]))

        tempSurface.stamp(surface, (0, 0), visibleRect)
        tempSurface.resize((visibleRect[2] * scalex, visibleRect[3] * scaley))

        # pe.draw.rect((255-ext['background'][0], 255-ext['background'][1], 255-ext['background'][2]), (posx - 1, posy - 1, rect[0]*scalex + 2, rect[1]*scaley + 2), 0)
        if debug:
            pe.draw.rect(pe.colors.red, (posx, posy, rect[0] * scalex, rect[1] * scaley), 20)
        pe.display.blit(tempSurface, worldtoscreen(visibleRect[0], visibleRect[1]))
        if debug:
            cropped2 = pe.pygame.transform.scale(surface, ((rect[0] * scalex) / 10, (rect[1] * scaley) / 10))
            pe.display.blit(cropped2, (10, 10))
            pe.draw.rect(pe.colors.red, (10, 10, (rect[0] * scalex) / 10, (rect[1] * scaley) / 10), 2)
            pe.draw.rect(pe.colors.red, (
            10 + (visibleRect[0] * scalex) / 10, 10 + (visibleRect[1] * scaley) / 10, (visibleRect[2] * scalex) / 10,
            (visibleRect[3] * scaley) / 10), 2)

        # Tap mode select
        if 'gameover' not in game_state:
            pe.draw.circle(ext['text'], (ss[0] / 2 - 30, ss[1] - ss[1] / 10), 31, 0)
            pe.draw.circle(ext['text'], (ss[0] / 2 + 30, ss[1] - ss[1] / 10), 31, 0)
            pe.draw.rect(ext['text'], (ss[0] / 2 - 30, ss[1] - ss[1] / 10 - 31, 60, 62), 0)
            pe.draw.circle(ext['background'], (ss[0] / 2 - 30, ss[1] - ss[1] / 10), 30, 0)
            pe.draw.circle(ext['background'], (ss[0] / 2 + 30, ss[1] - ss[1] / 10), 30, 0)
            pe.draw.rect(ext['background'], (ss[0] / 2 - 30, ss[1] - ss[1] / 10 - 30, 60, 60), 0)
            if tapMode == 'bomb':
                pe.draw.circle(ext['color'], (ss[0] / 2 - 30, ss[1] - ss[1] / 10), 25, 0)
                res['mineBackground'].display()
                touchButton.image((ss[0] / 2 + 30 - 25, ss[1] - ss[1] / 10 - 25, 50, 50), res['flagText'],
                                  res['flagColor'], tapModeFlag)
            elif tapMode == 'flag':
                pe.draw.circle(ext['color'], (ss[0] / 2 + 30, ss[1] - ss[1] / 10), 25, 0)
                res['flagBackground'].display()
                touchButton.image((ss[0] / 2 - 30 - 25, ss[1] - ss[1] / 10 - 25, 50, 50), res['mineText'],
                                  res['mineColor'], tapModeBomb)

        # Debug draw and update
        if debug:
            pe.draw.circle(pe.colors.white, worldtoscreen(*screentoworld(*pe.mouse.pos())), 5, 2)
        if debug and zooming:
            try:
                pe.draw.line(pe.colors.blue, worldtoscreen(*zoom_start_pos),
                             worldtoscreen(afterzoomx, zoom_start_pos[1]), 1)
                pe.draw.line(pe.colors.blue, worldtoscreen(afterzoomx, zoom_start_pos[1]),
                             worldtoscreen(afterzoomx, afterzoomy), 1)
                pe.draw.line(pe.colors.red, worldtoscreen(*zoom_start_pos), worldtoscreen(afterzoomx, afterzoomy), 1)
            except:
                print("waiting for values")
    elif game_state == 'menuInit':
        res['mine'].pos = ((ss[0] / 2) - 100, (ss[1] / 2) - 225)
        res['arrowLeft'].pos = ((ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 50)
        res['arrowLeftSelected'].pos = ((ss[0] / 2) - presets['buttonSpace'] - 35, (ss[1] / 2) + 50)

        res['arrowRight'].pos = ((ss[0] / 2) + presets['buttonSpace'], (ss[1] / 2) + 50)
        res['arrowRightSelected'].pos = ((ss[0] / 2) + presets['buttonSpace'] + 5, (ss[1] / 2) + 50)

        res['flagText'].pos = (ss[0] / 2 + 30 - 15, ss[1] - ss[1] / 10 - 15)
        res['flagBackground'].pos = (ss[0] / 2 + 30 - 15, ss[1] - ss[1] / 10 - 15)
        res['flagColor'].pos = (ss[0] / 2 + 30 - 15, ss[1] - ss[1] / 10 - 15)
        res['mineText'].pos = (ss[0] / 2 - 30 - 15, ss[1] - ss[1] / 10 - 15)
        res['mineBackground'].pos = (ss[0] / 2 - 30 - 15, ss[1] - ss[1] / 10 - 15)
        res['mineColor'].pos = (ss[0] / 2 - 30 - 15, ss[1] - ss[1] / 10 - 15)
        game_state = 'menu'
    elif game_state == 'menu':
        rect = (ss[0] - 70, 40, 30, 30)
        if themesMenu and not themesMenu2:
            themeMenu()
            pe.draw.circle(ext['text'], pe.math.center(rect), 32, 0)
            pe.draw.circle(ext['color'], pe.math.center(rect), 30, 0)
            touchButton.image(rect, res['themesBackground'], res['themesText'], toggleThemeMenu)
        elif len(fingers) == 0 and themesMenu2:
            themesMenu2 = False
        if (not themesMenu) and not themesMenu2:
            pe.draw.circle(ext['color'], pe.math.center((ss[0] - 70, 40, 30, 30)), 30, 1)
            touchButton.image(rect, res['themesText'], res['themesBackground'], toggleThemeMenu)
        elif len(fingers) == 0 and themesMenu2:
            themesMenu2 = False
        res['mine'].display()
        # Gamemode selector
        touchButton.image(((ss[0] / 2) - presets['buttonSpace'] - 40, (ss[1] / 2) + 40, 50, 50), res['arrowLeft'],
                          res['arrowLeftSelected'], leftArrow)
        touchButton.image(((ss[0] / 2) + presets['buttonSpace'] - 10, (ss[1] / 2) + 40, 50, 50), res['arrowRight'],
                          res['arrowRightSelected'], rightArrow)
        res['gamemodeText'][ext['gamemode']].display()

        # New game button
        touchButton.rect(
            ((ss[0] / 2) - presets['buttonSpace'] - 70, (ss[1] / 2) + 100, presets['buttonSpace'] * 2 + 100, 40),
            ext['background'], ext['background'], action=startNewGame)
        if pe.rect.Rect(*pe.mouse.pos(), 1, 1).colliderect(
                pe.rect.Rect((ss[0] / 2) - presets['buttonSpace'] - 70, (ss[1] / 2) + 100,
                             presets['buttonSpace'] * 2 + 100, 40)):
            pe.draw.circle(ext['color'], ((ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 120), 20, 0)
            pe.draw.circle(ext['color'], ((ss[0] / 2) + presets['buttonSpace'] + 30, (ss[1] / 2) + 120), 20, 0)
            pe.draw.rect(ext['color'], (
            (ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100, presets['buttonSpace'] * 2 + 60, 40), 0)
            res['startGameTextSelected'].display()
        else:
            pe.draw.circle(ext['text'], ((ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 120), 20,
                           presets['buttonLineSize'])
            pe.draw.circle(ext['text'], ((ss[0] / 2) + presets['buttonSpace'] + 30, (ss[1] / 2) + 120), 20,
                           presets['buttonLineSize'])
            pe.draw.rect(ext['background'], (
            (ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100, presets['buttonSpace'] * 2 + 60, 40), 0)
            pe.draw.line(ext['text'], ((ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100),
                         ((ss[0] / 2) + presets['buttonSpace'] + 30, (ss[1] / 2) + 100), presets['buttonLineSize']
                         )
            pe.draw.line(ext['text'],
                         ((ss[0] / 2) - presets['buttonSpace'] - 30, (ss[1] / 2) + 140 - presets['buttonLineSize']),
                         ((ss[0] / 2) + presets['buttonSpace'] + 30, (ss[1] / 2) + 140 - presets['buttonLineSize']),
                         presets['buttonLineSize']
                         )
            res['startGameText'].display()
    elif game_state == 'pregame':
        # save()
        pe.draw.circle((ext['color'][0] - 10, ext['color'][1] - 10, ext['color'][2] - 10), (ss[0] / 2, ss[1] / 2),
                       pregame_animation + 10, 0)
        pe.draw.circle(ext['color'], (ss[0] / 2, ss[1] / 2), pregame_animation, 0)
        if pregame_animation < pe.math.dist((posx, posy), (ss[0] / 2, ss[1] / 2)):
            pregame_animation += 1
        else:
            pregame_animation = 255
            game_state = 'startgame'
        pe.draw.rect(ext['background'], (0, 0, ss[0], posy), 0)
        pe.draw.rect(ext['background'], (0, posy + rect[1] * scaley, ss[0], ss[1] - (posy + rect[1] * scaley)), 0)
        pe.draw.rect(ext['background'], (0, 0, posx, ss[1]), 0)
        pe.draw.rect(ext['background'], (posx + rect[0] * scalex, 0, ss[0] - (posx + rect[0] * scalex), ss[1]), 0)
    elif game_state == 'startgame':
        pe.draw.rect(ext['color'], (posx, posy, rect[0] * scalex, rect[1] * scaley), 0)
        res['beginGameText'].display()
        pe.draw.rect((*ext['color'], max(0, pregame_animation)), (posx, posy, rect[0] * scalex, rect[1] * scaley), 0)
        if pregame_animation > 0:
            pregame_animation -= 2
        if pe.mouse.clicked()[0]:
            scale_animationEnable = True
            loc = screentoworld(*pe.mouse.pos())
            start_scalex = scalex
            start_scaley = scaley
            scale_animationPX = pe.mouse.pos()[0]
            scale_animationPY = pe.mouse.pos()[1]
            scale_animationX = 2
            scale_animationY = 2
            gamemode = ext['gamemode']
            gamemode = presets['gamemodes'][gamemode]
            rect = (30 * gamemode['grid'][0], 30 * gamemode['grid'][1])
            gridX = int(loc[0] / 30)
            gridY = int(loc[1] / 30)
            generateBoard(*gamemode['grid'], *gamemode['bombs'], gridX, gridY)
            filterClosed = flood.filtered(boardMap, 'closed')
            filterFlagged = flood.filtered(boardMap, 'flagged')
            gameJustBegun = True
            game_state = 'ingame'
    elif game_state == 'gameoverInit':
        res['arrowLeft'].pos = ((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, ss[1] / 2)
        res['arrowLeftSelected'].pos = ((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 35, ss[1] / 2)

        res['arrowRight'].pos = ((ss[0] - ss[0] / 6) + presets['buttonSpace'], ss[1] / 2)
        res['arrowRightSelected'].pos = ((ss[0] - ss[0] / 6) + presets['buttonSpace'] + 5, ss[1] / 2)
        game_state = 'gameover'
    if game_state == 'pregameover':
        gamemode = ext['gamemode']
        gamemode = presets['gamemodes'][gamemode]
        rect = (30 * gamemode['grid'][0], 30 * gamemode['grid'][1])
        scalex = ((ss[1] - 100) / rect[1])
        scaley = scalex
        posx = ss[0] / 2 - rect[0] * scalex / 2  # center X
        posy = ss[1] / 2 - rect[1] * scaley / 2  # center Y
        ok = False
        if not ok:
            game_state = 'gameoverInit'
    elif game_state == 'gameover':
        touchButton.image(((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 40, (ss[1] / 2), 50, 50), res['arrowLeft'],
                          res['arrowLeftSelected'], leftArrow)
        touchButton.image(((ss[0] - ss[0] / 6) + presets['buttonSpace'] - 10, (ss[1] / 2), 50, 50), res['arrowRight'],
                          res['arrowRightSelected'], rightArrow)
        res['gamemodeTextOver'][ext['gamemode']].display()

        touchButton.rect(((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 70, (ss[1] / 2) + 100,
                          presets['buttonSpace'] * 2 + 100, 40), ext['background'], ext['background'],
                         action=startNewGame)
        if pe.rect.Rect(*pe.mouse.pos(), 1, 1).colliderect(
                pe.rect.Rect((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 70, (ss[1] / 2) + 100,
                             presets['buttonSpace'] * 2 + 100, 40)):
            pe.draw.circle(ext['color'], ((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 120), 20, 0)
            pe.draw.circle(ext['color'], ((ss[0] - ss[0] / 6) + presets['buttonSpace'] + 30, (ss[1] / 2) + 120), 20, 0)
            pe.draw.rect(ext['color'], (
            (ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100, presets['buttonSpace'] * 2 + 60, 40),
                         0)
            res['startGameTextSelectedOver'].display()
        else:
            pe.draw.circle(ext['text'], ((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 120), 20,
                           presets['buttonLineSize'])
            pe.draw.circle(ext['text'], ((ss[0] - ss[0] / 6) + presets['buttonSpace'] + 30, (ss[1] / 2) + 120), 20,
                           presets['buttonLineSize'])
            pe.draw.rect(ext['background'], (
            (ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100, presets['buttonSpace'] * 2 + 60, 40),
                         0)
            pe.draw.line(ext['text'], ((ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 100),
                         ((ss[0] - ss[0] / 6) + presets['buttonSpace'] + 30, (ss[1] / 2) + 100),
                         presets['buttonLineSize']
                         )
            pe.draw.line(ext['text'], (
            (ss[0] - ss[0] / 6) - presets['buttonSpace'] - 30, (ss[1] / 2) + 140 - presets['buttonLineSize']),
                         ((ss[0] - ss[0] / 6) + presets['buttonSpace'] + 30,
                          (ss[1] / 2) + 140 - presets['buttonLineSize']), presets['buttonLineSize']
                         )
            res['startGameTextOver'].display()
    log.render()
    pe.display.update()
    if len(fingers) == 0:
        buttons = {}
    if activate_debug:
        pe.stop_recording()
        pe.start_debug()
        activate_debug = False
