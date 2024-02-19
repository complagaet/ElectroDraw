HEIGHT, WIDTH = 0, 0


def LAYOUT_HW_UPDATE(h, w):
    global HEIGHT
    global WIDTH
    HEIGHT = h
    WIDTH = w


def align_relatively(anchor, x, y):
    return anchor[0] + x, anchor[1] + y


def align(surf, x, y, corner):
    ret = [0, 0]
    if corner == "ct":  # Center-Top
        ret[0] = WIDTH - (surf.get_width() / 2) - (WIDTH / 2) - x
        ret[1] = y

    if corner == "c":  # Center
        ret[0] = WIDTH - (surf.get_width() / 2) - (WIDTH / 2) - x
        ret[1] = HEIGHT - (surf.get_height() / 2) - (HEIGHT / 2) - y

    if corner == "rb":  # Right-Bottom
        ret[0] = WIDTH - surf.get_width() - x
        ret[1] = HEIGHT - surf.get_height() - y

    if corner == "lc":  # Left-Bottom
        ret[0] = x
        ret[1] = HEIGHT - (surf.get_height() / 2) - (HEIGHT / 2) - y

    if corner == "cb":  # Center-Bottom
        ret[0] = WIDTH - (surf.get_width() / 2) - (WIDTH / 2) - x
        ret[1] = HEIGHT - surf.get_height() - y

    if corner == "lb":  # Left-Bottom
        ret[0] = x
        ret[1] = HEIGHT - surf.get_height() - y

    if corner == "lt":  # Left-Top
        ret[0] = x
        ret[1] = y

    return ret[0], ret[1]  # Returns tuple


def multi_line(scr, font, f_size, color, text, x, y, al):
    lines = reversed(text.splitlines())
    for i, l in enumerate(lines):
        g = font.render(l, False, color)
        scr.blit(g, align(g, x, y + f_size * i, al))


def IN_check_2D(left_top, right_bottom, pos):
    return left_top[0] <= pos[0] < right_bottom[0] and left_top[1] <= pos[1] < right_bottom[1]


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
