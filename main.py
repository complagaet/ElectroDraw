import script.content as cont
from script.tools import *
from script.storage import *
import pygame
import copy
import platform

DEBUG = False
LAST_MOUSE_POSITION = (0, 0)
L_MOUSE_HOLD = False
R_MOUSE_HOLD = False
CTRL_HOLD = False
LOCATION = "START"
LOCATION_SUB = ""
VER = "0.0"
PALETTE = list(map(lambda x: list(map(lambda a: hex_to_rgb(a), x)), [
    ["000000", "800080", "FF0000", "FF1493", "AF708B", "F0D9E8", "FF69B4", "00FFFF"],
    ["FFFFFF", "FFFF00", "0000FF", "FFA500", "008000", "87CEEB", "FFFACD", "FFA07A"],
    ["808080", "00FF00", "FF00FF", "3B7EFF", "FFD700", "20B2AA", "6A5ACD", "E0FFFF"]
]))
PROJ = {
    "Name": "",
    "CanvasSize": (0, 0),
    "Draw": [],
    "Params": {
        "PrimaryColor": (0, 0, 0),
        "SecondaryColor": (255, 255, 255),
        "CanvasActive": True,
        "History": []
    }
}
CTRL_Z_COUNT = 50
CTRL_Z_POS = 0


class Screens:
    def __init__(self, scr):
        self.scr = scr
        self.DRAW_CHANGED = False
        self.LAST_DRAW_MOUSE_CORD = (0, 0)
        self.IN_CANVAS = False

    def loadscreen(self):
        scr = self.scr
        scr.blit(IMG['AITU'], align(IMG['AITU'], 14, 14, "lb"))
        scr.blit(IMG['Lukoyanov'], align(IMG['Lukoyanov'], 14, 10, "rb"))
        scr.blit(IMG['EDLogoBig'], align(IMG['EDLogoBig'], 0, -75, "ct"))
        multi_line(scr, FONT["Main"], 16, CL['BLACK'], LANG["PashaAITU"], 76, 17, "lb")

    def alert(self, img, header, info, bgcolor='BGFocus'):
        scr = self.scr

        ramka = pygame.Surface((240, 80), pygame.SRCALPHA)
        ramkaPos = align(ramka, 0, 0, "c")

        pygame.draw.rect(ramka, CL[bgcolor], pygame.Rect(0, 0, 240, 80), 0, 15)
        pygame.draw.rect(ramka, CL['BLACK'], pygame.Rect(0, 0, 240, 80), 1, 15)
        scr.blit(ramka, ramkaPos)

        scr.blit(img, align_relatively(ramkaPos, 8, 8))

        scr.blit(FONT["Main"].render(header, False, CL['BLACK']), align_relatively(ramkaPos, 47, 17))
        scr.blit(FONT["Main"].render(info, False, CL['BLACK']), align_relatively(ramkaPos, 8, 57))

    def proj_header(self, name):
        scr = self.scr
        w, h = WIDTH - 20, 30

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(ramka, CL['BGFocus'], pygame.Rect(0, 0, w, h), 0, 4)
        scr.blit(ramka, align(ramka, 0, 10, "ct"))

        name = FONT["Main"].render(name, False, CL['BLACK'])
        scr.blit(name, align(name, 0, 18, "ct"))

    def help(self, lst):  # [(ico, text), ...]
        scr = self.scr
        w, h = 300, (32 * len(lst)) + 16 + (8 * (len(lst) - 1))

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        ramkaPos = align(ramka, 0, 10, "cb")
        pygame.draw.rect(ramka, CL['WHITE'], pygame.Rect(0, 0, w, h), 0, 15)
        pygame.draw.rect(ramka, CL['BLACK'], pygame.Rect(0, 0, w, h), 1, 15)
        scr.blit(ramka, ramkaPos)

        count = 0
        for g in lst:
            scr.blit(g[0], align_relatively(ramkaPos, 8, 8 + (32 * count) + (8 * count)))
            scr.blit(
                FONT["Main"].render(g[1], False, CL['BLACK']),
                align_relatively(ramkaPos, 47, 17 + (16 * count) + (24 * count))
            )
            count += 1

    def menu(self, ev, header, lst, focused, multiple):
        global L_MOUSE_HOLD
        scr = self.scr
        w, h = 240, 20 + (32 * len(lst)) + 16 + (8 * (len(lst) - 1))

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        ramkaPos = align(ramka, 0, 0, "c")
        pygame.draw.rect(ramka, CL['WHITE'], pygame.Rect(0, 0, w, h), 0, 15)
        pygame.draw.rect(ramka, CL['BLACK'], pygame.Rect(0, 0, w, h), 1, 15)
        scr.blit(ramka, ramkaPos)

        scr.blit(FONT["Main"].render(header, False, CL['BLACK']), align_relatively(ramkaPos, 8, 8))

        count = 0
        for g in lst:
            o = IMG['Entry']
            if focused[count] == 1:
                o = IMG['EntryFocused']

            entry_pos = align_relatively(ramkaPos, 8, 28 + (32 * count) + (8 * count))
            scr.blit(o, entry_pos)

            mouse = LAST_MOUSE_POSITION
            entry_pos_corner = (entry_pos[0] + w - 10, entry_pos[1] + 32)
            if IN_check_2D(entry_pos, entry_pos_corner, mouse):
                scr.blit(IMG['EntryFocused'], entry_pos)

            if IN_check_2D(entry_pos, entry_pos_corner, mouse) and L_MOUSE_HOLD:
                if multiple:
                    focused[count] = not focused[count]
                else:
                    focused = list(map(lambda a: 0, focused))
                    focused[count] = 1
                SOUND['Click'].play()
                L_MOUSE_HOLD = False

            scr.blit(g[0], align_relatively(ramkaPos, 32, 28 + (32 * count) + (8 * count)))
            scr.blit(
                FONT["Main"].render(g[1], False, CL['BLACK']),
                align_relatively(ramkaPos, 71, 37 + (16 * count) + (24 * count))
            )
            count += 1

        return focused

    def canvas(self, evn, res, draw):
        scr = self.scr
        hw = min([32, 48, 64, 72, 128, 256, 512], key=lambda x: abs(x - HEIGHT - 60))
        w, h = hw, hw

        if len(draw) == 0:
            for i in range(0, res[0]):
                draw.append([])
                st = draw[i]
                for j in range(0, res[1]):
                    st.append((255, 255, 255))
            CTRL_Z("SAVE")

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        if WIDTH < w + 120 * 2 or HEIGHT < h + 50 * 2:
            ramkaPos = align(ramka, 120, 50, "lt")
        else:
            ramkaPos = align(ramka, 0, 0, "c")
        pygame.draw.rect(ramka, CL['WHITE'], pygame.Rect(0, 0, w, h), 0)
        pygame.draw.rect(ramka, CL['BLACK'], pygame.Rect(0, 0, w, h), 1)

        for i in range(0, res[0]):
            for j in range(0, res[1]):
                pygame.draw.rect(
                    ramka, draw[i][j],
                    pygame.Rect(
                        (w / res[0] * i, h / res[1] * j),
                        (w / res[0], h / res[1])
                    )
                )

        global L_MOUSE_HOLD, R_MOUSE_HOLD
        br = False
        if PROJ['Params']['CanvasActive']:
            for i in range(0, res[0]):
                for j in range(0, res[1]):
                    ramka_LT = (ramkaPos[0] + w / res[0] * i, ramkaPos[1] + h / res[1] * j)
                    ramka_RB = (ramkaPos[0] + w / res[0] * i + w / res[0], ramkaPos[1] + h / res[1] * j + h / res[0])
                    if IN_check_2D(ramka_LT, ramka_RB, LAST_MOUSE_POSITION):
                        if (not self.IN_CANVAS) and self.DRAW_CHANGED:
                            self.LAST_DRAW_MOUSE_CORD = (i, j)

                        self.IN_CANVAS = True
                        DRAW_MOUSE_CORD = (i, j)
                        if not (L_MOUSE_HOLD or R_MOUSE_HOLD):
                            self.LAST_DRAW_MOUSE_CORD = (i, j)
                        pygame.draw.rect(
                            ramka, (0, 0, 0),
                            pygame.Rect(
                                (w / res[0] * i, h / res[1] * j),
                                (w / res[0], h / res[1])
                            ), 1
                        )

                        COLOR = ()
                        if L_MOUSE_HOLD:
                            COLOR = PROJ['Params']['PrimaryColor']
                        elif R_MOUSE_HOLD:
                            COLOR = PROJ['Params']['SecondaryColor']

                        if L_MOUSE_HOLD or R_MOUSE_HOLD:
                            draw_line(PROJ['Draw'], self.LAST_DRAW_MOUSE_CORD, DRAW_MOUSE_CORD, COLOR)
                            PROJ['Draw'][i][j] = COLOR
                            self.LAST_DRAW_MOUSE_CORD = DRAW_MOUSE_CORD
                            self.DRAW_CHANGED = True

                        br = True

        if not br:
            self.IN_CANVAS = False

        scr.blit(
            FONT['Main'].render(f"{res[0]}x{res[1]} | {w}x{h}", False, CL['BLACK']),
            align_relatively(ramkaPos, 0, h + 2)
        )
        scr.blit(ramka, ramkaPos)

    def color_preview(self, color):
        scr = self.scr
        w, h = 45, 45

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        ramkaPos = align(ramka, -120, 0, "c")
        pygame.draw.rect(ramka, color, pygame.Rect(0, 0, w, h), 0, 15)
        pygame.draw.rect(ramka, CL['BLACK'], pygame.Rect(0, 0, w, h), 1, 15)
        scr.blit(ramka, ramkaPos)

    def tools(self, res):
        global L_MOUSE_HOLD, R_MOUSE_HOLD
        scr = self.scr
        w, h = 100, HEIGHT - 60

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        ramkaPos = align(ramka, 10, 50, "lt")
        pygame.draw.rect(ramka, CL['Tools'], pygame.Rect(0, 0, w, h), 0, 4)

        BACKWARD_LT, FORWARD_LT, BF_SIZE = (15, 16), (43, 16), (21, 19)
        if CTRL_Z_POS != 0:
            scr.blit(IMG['BackwardFocused'], BACKWARD_LT)
            if (
                    IN_check_2D(BACKWARD_LT,
                                (BACKWARD_LT[0] + BF_SIZE[0], BACKWARD_LT[1] + BF_SIZE[1]),
                                LAST_MOUSE_POSITION) and L_MOUSE_HOLD
            ):
                CTRL_Z('BACK')
                SOUND['Click'].play()
                L_MOUSE_HOLD = False
        else:
            scr.blit(IMG['Backward'], BACKWARD_LT)
        if CTRL_Z_POS < len(PROJ['Params']['History']) - 1 and len(PROJ['Params']['History']) != 0:
            scr.blit(IMG['ForwardFocused'], FORWARD_LT)
            if (
                    IN_check_2D(FORWARD_LT,
                                (FORWARD_LT[0] + BF_SIZE[0], FORWARD_LT[1] + BF_SIZE[1]),
                                LAST_MOUSE_POSITION) and L_MOUSE_HOLD
            ):
                CTRL_Z('FORWARD')
                SOUND['Click'].play()
                L_MOUSE_HOLD = False
        else:
            scr.blit(IMG['Forward'], FORWARD_LT)

        pygame.draw.rect(ramka, CL['GRAY'], pygame.Rect(5, 43, 90, 1))
        pygame.draw.rect(ramka, CL['GRAY'], pygame.Rect(5, 90, 90, 1))

        count, afterPaletteY = [0, 0], 0
        for i in PALETTE:
            for j in i:
                LT = (11 + (21 * count[0]) + (7 * count[0]), 99 + (21 * count[1]) + (7 * count[1]))
                afterPaletteY = LT[1] + 28
                pygame.draw.rect(ramka, j, pygame.Rect(LT[0], LT[1], 21, 21), 0, 4)
                LT = (LT[0] + ramkaPos[0], LT[1] + ramkaPos[1])
                if IN_check_2D(LT, (LT[0] + 21, LT[1] + 21), LAST_MOUSE_POSITION):
                    if L_MOUSE_HOLD:
                        PROJ["Params"]["PrimaryColor"] = j
                        SOUND['Click'].play()
                        L_MOUSE_HOLD = False
                    if R_MOUSE_HOLD:
                        PROJ["Params"]["SecondaryColor"] = j
                        SOUND['Click'].play()
                        R_MOUSE_HOLD = False
                count[1] += 1
            count[0] += 1
            count[1] = 0
        pygame.draw.rect(ramka, PROJ["Params"]["SecondaryColor"], pygame.Rect(44, afterPaletteY + 10, 21, 21), 0, 4)
        pygame.draw.rect(ramka, CL['WHITE'], pygame.Rect(44, afterPaletteY + 10, 21, 21), 1, 4)
        pygame.draw.rect(ramka, PROJ["Params"]["PrimaryColor"], pygame.Rect(34, afterPaletteY, 21, 21), 0, 4)
        pygame.draw.rect(ramka, CL['WHITE'], pygame.Rect(34, afterPaletteY, 21, 21), 1, 4)
        pygame.draw.rect(ramka, CL['GRAY'], pygame.Rect(5, afterPaletteY + 38, 90, 1))
        SWAP_LT = (ramkaPos[0] + 72, ramkaPos[1] + afterPaletteY + 6)
        SWAP_CLICK_ZONE_LT = (ramkaPos[0] + 34, ramkaPos[1] + afterPaletteY)
        if (
                IN_check_2D(SWAP_CLICK_ZONE_LT,
                            (SWAP_CLICK_ZONE_LT[0] + 60, SWAP_CLICK_ZONE_LT[1] + 35),
                            LAST_MOUSE_POSITION) and L_MOUSE_HOLD
        ):
            color_swap(PROJ)
            SOUND['Click'].play()
            L_MOUSE_HOLD = False

        HEX_LT = (15, afterPaletteY + 96)
        if IN_check_2D(HEX_LT, (HEX_LT[0] + 90, HEX_LT[1] + 32), LAST_MOUSE_POSITION):
            if L_MOUSE_HOLD:
                PROJ['Params']['CanvasActive'] = False
                global LOCATION_SUB, hex_color
                LOCATION_SUB = "HEX"
                hex_color = rgb_to_hex(PROJ["Params"]["PrimaryColor"])
                SOUND['Click'].play()
                L_MOUSE_HOLD = False

        afterPaletteY += 96 + 32

        scr.blit(ramka, ramkaPos)
        scr.blit(IMG['Swap'], SWAP_LT)
        scr.blit(IMG['HEXBig'], HEX_LT)
        scr.blit(IMG['EDLogoGUI'], (16, 58))
        scr.blit(IMG[f'{res[0]}'], (44, 59 + 42))

    def right_bottom_menu_btn(self, name):
        scr = self.scr
        w, h = 100, 32

        ramka = pygame.Surface((w, h), pygame.SRCALPHA)
        ramkaPos = align(ramka, 10, 10, "rb")
        pygame.draw.rect(ramka, CL["Tools"], pygame.Rect(0, 0, w, h), 0, 4)
        scr.blit(ramka, ramkaPos)

        t = FONT['Main'].render(name, False, CL['WHITE'])
        scr.blit(t, (ramkaPos[0] + w / 2 - t.get_width() / 2, ramkaPos[1] + h / 2 - t.get_height() / 2))

        global LOCATION_SUB, L_MOUSE_HOLD
        if IN_check_2D(ramkaPos, (ramkaPos[0] + w, ramkaPos[1] + h), LAST_MOUSE_POSITION):
            if L_MOUSE_HOLD:
                LOCATION_SUB = "PROJ_MENU"
                SOUND['Click'].play()
                L_MOUSE_HOLD = False


def CTRL_Z(action):
    global CTRL_Z_POS
    history = PROJ['Params']['History']
    if action == "SAVE":
        if CTRL_Z_POS != len(history) - 1:
            for i in range(CTRL_Z_POS, len(history) - 1):
                history.pop()

        history.append(copy.deepcopy(PROJ['Draw']))
        CTRL_Z_POS = len(history) - 1

        if len(history) > CTRL_Z_COUNT:
            history.pop(0)

    elif action == "BACK":
        if CTRL_Z_POS > 0:
            PROJ['Draw'] = copy.deepcopy(history[CTRL_Z_POS - 1])
            CTRL_Z_POS -= 1

    elif action == "FORWARD":
        if CTRL_Z_POS < len(history) - 1:
            PROJ['Draw'] = copy.deepcopy(history[CTRL_Z_POS + 1])
            CTRL_Z_POS += 1


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT, FPS = 980, 780, 60
LAYOUT_HW_UPDATE(HEIGHT, WIDTH)
CL = cont.getCL()
IMG = cont.getIMG()
SOUND = cont.getSOUND()
FONT = cont.getFONT()
LANG = cont.lang()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
screens = Screens(screen)

pygame.display.set_caption(LANG['ED'])
pygame.display.set_icon(pygame.image.load('content/EDIco.png'))
clock = pygame.time.Clock()

c = 0
sub_opened = False
new_project_canvas_size_params = [0, 0, 0, 0, 0, 0]
hex_color = ""

running = True
while running:
    clock.tick(FPS)
    screen.fill(CL['BG'])
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            WIDTH = screen.get_width()
            HEIGHT = screen.get_height()
            LAYOUT_HW_UPDATE(HEIGHT, WIDTH)

        if event.type == pygame.MOUSEMOTION:
            LAST_MOUSE_POSITION = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                L_MOUSE_HOLD = True
            elif event.button == 3:
                R_MOUSE_HOLD = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                L_MOUSE_HOLD = False
            elif event.button == 3:
                R_MOUSE_HOLD = False

        if event.type == pygame.KEYDOWN:
            if (
                    ((event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and platform.system() != "Darwin")
                    or (event.key == 1073742051 or event.key == 1073742055)
            ):
                CTRL_HOLD = True

        if event.type == pygame.KEYUP:
            if (
                    ((event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and platform.system() != "Darwin")
                    or (event.key == 1073742051 or event.key == 1073742055)
            ):
                CTRL_HOLD = False

    if LOCATION == "START":
        pygame.display.set_caption(LANG['ED'])
        screens.loadscreen()
        keys = screens.menu(
            ev, f"{LANG['ED']} ver. {VER}",
            [
                (IMG['Molotok'], LANG['NewProj']),
                (IMG['Reset'], LANG['Exit'])
            ],
            [0, 0], False
        )

        if keys[0]:
            LOCATION = "LOAD"

        if keys[1]:
            running = False

        PROJ['Name'] = ""
        PROJ['CanvasSize'] = (0, 0)
        PROJ['Draw'] = []

        if pygame.KEYDOWN in list(map(lambda a: a.type, ev)):
            LOCATION = "LOAD"

    elif LOCATION == "LOAD":
        screens.loadscreen()
        screens.alert(IMG['EDIcoGUI'], LANG['ED'], f"{LANG['Wait']} {c}", "BGFocus")
        c += 1

        if c >= 20:
            LOCATION = "NEWPROJECT"
            c = 0

    elif LOCATION == "NEWPROJECT":
        pygame.display.set_caption(f"{LANG['ED']} | {LANG['NewProj']}")
        for event in ev:
            if event.type == pygame.TEXTINPUT:
                PROJ['Name'] += f"{event.text}"

            if event.type == pygame.KEYDOWN:
                if event.key == 8:
                    PROJ['Name'] = PROJ['Name'][:-1]

                if event.key == 13:
                    LOCATION = "NEWPROJECT_2"

                if event.key == 27:
                    LOCATION = "START"

        screens.alert(IMG['Molotok'], LANG['NewProj'], f"{LANG['Name']}: {PROJ['Name'] + '_'}", "WHITE")
        screens.proj_header(PROJ['Name'])
        screens.help([(IMG['Back'], LANG['Help_ESC']), (IMG['Next'], LANG['Help_Enter'])])

    elif LOCATION == "NEWPROJECT_2":
        pygame.display.set_caption(f"{LANG['ED']} | {LANG['NewProj']}")
        new_project_canvas_size_params = screens.menu(
            ev, LANG['CanvasSize'],
            [
                (IMG['8'], "8x8"),
                (IMG['16'], "16x16"),
                (IMG['32'], "32x32"),
                (IMG['64'], "64x64"),
                (IMG['128'], "128x128"),
                (IMG['256'], "256x256 (Laggy!)")
            ],
            new_project_canvas_size_params, False
        )
        screens.proj_header(PROJ['Name'])
        screens.help([(IMG['Back'], LANG['Help_ESC_Back'])])

        sizes = [(8, 8), (16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]
        if 1 in new_project_canvas_size_params:
            PROJ['CanvasSize'] = sizes[new_project_canvas_size_params.index(1)]
            new_project_canvas_size_params = list(map(lambda a: 0, new_project_canvas_size_params))
            PROJ['Draw'] = []
            PROJ['Params']['History'] = []
            c = 0
            LOCATION = "DRAW"

        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    LOCATION = "NEWPROJECT"

    elif LOCATION == "DRAW":
        pygame.display.set_caption(f"{LANG['ED']} | {PROJ['Name']}")

        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == 27 and LOCATION_SUB == "":
                    sub_opened = False
                    LOCATION_SUB = "PROJ_MENU"

                if event.scancode == 29 and CTRL_HOLD:
                    CTRL_Z('BACK')

                if event.scancode == 28 and CTRL_HOLD:
                    CTRL_Z('FORWARD')

                if event.scancode == 22:
                    color_swap(PROJ)

        if c == 20:
            screens.canvas(ev, PROJ['CanvasSize'], PROJ['Draw'])
            if screens.DRAW_CHANGED and not (L_MOUSE_HOLD or R_MOUSE_HOLD):
                CTRL_Z('SAVE')
                screens.DRAW_CHANGED = False
        else:
            c += 1
            screens.alert(IMG['EDIcoGUI'], LANG['ED'], f"{LANG['Wait']}", "BGFocus")

        screens.proj_header(PROJ['Name'])
        screens.right_bottom_menu_btn(LANG['Menu'])
        screens.tools(PROJ['CanvasSize'])

    elif LOCATION == "EXIT_DRAW":
        screens.proj_header(PROJ['Name'])

        keys = screens.menu(
            ev, LANG['ConfirmLeave'],
            [
                (IMG['Return'], LANG['No']),
                (IMG['Reset'], LANG['Yes'])
            ],
            [0, 0], False
        )

        if keys[0]:
            LOCATION = "DRAW"
            L_MOUSE_HOLD = False

        if keys[1]:
            LOCATION = "START"

    if DEBUG:
        if len(ev) != 0:
            k = ev
        multi_line(screen, FONT["Main"], 16, CL['BLUE'],
                   f"{LOCATION}\n{CTRL_HOLD}\nver. {VER}, {WIDTH}x{HEIGHT}\n{ev}\n{k}", 10, 10, "lt")

    # ----------------------

    if LOCATION_SUB == "HEX":
        screens.alert(IMG['HEXIco'], LANG['HEX'], f"#{hex_color.upper()}_", "WHITE")

        if hex_to_rgb(hex_color):
            screens.help([(IMG['Next'], LANG['Help_Use_Color']), (IMG['Back'], LANG['Help_ESC_Back'])])
            screens.color_preview(hex_to_rgb(hex_color))
        else:
            screens.help([(IMG['Next'], LANG['IncorrectColor']), (IMG['Back'], LANG['Help_ESC_Back'])])

        for event in ev:
            if event.type == pygame.TEXTINPUT:
                if len(hex_color) < 6:
                    hex_color += f"{event.text.upper()}"

            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    LOCATION_SUB = ""
                    PROJ['Params']['CanvasActive'] = True

                if event.key == 8:
                    hex_color = hex_color[:-1]

                if event.key == 13:
                    if hex_to_rgb(hex_color):
                        LOCATION_SUB = ""
                        PROJ['Params']['PrimaryColor'] = hex_to_rgb(hex_color)
                        PROJ['Params']['CanvasActive'] = True

    elif LOCATION_SUB == "PROJ_MENU":
        PROJ['Params']['CanvasActive'] = False
        for event in ev:
            if event.type == pygame.KEYDOWN:
                if event.key == 27 and sub_opened:
                    LOCATION_SUB = ""
                    PROJ['Params']['CanvasActive'] = True
                    sub_opened = False
        sub_opened = True

        keys = screens.menu(
            ev, LANG['Menu'],
            [
                (IMG['PNG'], LANG['ExportPNG']),
                (IMG['Back'], LANG['ReturnToCanvas']),
                (IMG['Home'], LANG['HomeScreen'])
            ],
            [0, 0, 0], False
        )

        if keys[0]:
            screen.fill(CL['BG'])
            screens.proj_header(PROJ['Name'])
            screens.alert(IMG['EDIcoGUI'], LANG['ED'], f"{LANG['Wait']}", "BGFocus")
            pygame.display.flip()
            if PROJ['CanvasSize'][0] >= 128:
                user_save_png(PROJ, 10)
            else:
                user_save_png(PROJ, 100)

        elif keys[1]:
            LOCATION_SUB = ""
            sub_opened = False
            PROJ['Params']['CanvasActive'] = True
            L_MOUSE_HOLD = False

        elif keys[2]:
            LOCATION_SUB = ""
            PROJ['Params']['CanvasActive'] = True
            LOCATION = "EXIT_DRAW"
            SOUND['Error'].play()

    pygame.display.flip()

pygame.quit()
