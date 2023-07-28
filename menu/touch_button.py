import pygameextra as pe

buttons = {}

def image(rect, ic, ac, action=None):
    global buttons
    fingers = pe.mouse.fingersupport.fingers
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
    global buttons
    fingers = pe.mouse.fingersupport.fingers
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