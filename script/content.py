import pygame


def getCL():
    return {
        "BG": (251, 243, 255),
        "BGFocus": (212, 191, 255),
        "Tools": (26, 26, 26),
        "GRAY": (100, 100, 100),
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255)
    }


def getIMG():
    return {
        "Lukoyanov": pygame.image.load('content/Lukoyanov.png'),
        "EDLogoBig": pygame.image.load('content/EDLogoBig.png'),
        "EDIcoGUI": pygame.image.load('content/EDIcoGUI.png'),
        "EDLogoGUI": pygame.image.load('content/EDLogoGUI.png'),
        "Molotok": pygame.image.load('content/Molotok.png'),
        "Back": pygame.image.load('content/Back.png'),
        "Next": pygame.image.load('content/Next.png'),
        "Entry": pygame.image.load('content/Entry.png'),
        "EntryFocused": pygame.image.load('content/EntryFocused.png'),
        "AITU": pygame.image.load('content/AITU.png'),
        "canvas": pygame.image.load('content/canvas.png'),
        "8": pygame.image.load('content/8.png'),
        "16": pygame.image.load('content/16.png'),
        "32": pygame.image.load('content/32.png'),
        "64": pygame.image.load('content/64.png'),
        "128": pygame.image.load('content/128.png'),
        "HEXBig": pygame.image.load('content/HEXBig.png'),
        "HEXIco": pygame.image.load('content/HEXIco.png')
    }


def getFONT():
    return {
        "Main": pygame.font.Font('content/PixCyrillic.ttf', 16)
    }


def lang():
    return {
        "ED": "ElectroDraw",
        "Wait": "Please wait...",
        "NewProj": "New project",
        "Name": "Name",
        "Error": "Error!",
        "Help_ESC": "ESC -> Home screen",
        "Help_ESC_Back": "ESC -> Back",
        "Help_Enter": "Enter -> Continue",
        "Help_Use_Color": "Enter -> Use color",
        "IncorrectColor": "Wrong color!",
        "CanvasSize": "Canvas size",
        "HEX": "HEX color",
        "PashaAITU": "Astana IT University\nLukoyanov Pavel\nSE-2331",
        "Welcome": "Welcome! Press any key to continue..."
    }
