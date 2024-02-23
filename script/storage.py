from PIL import Image  # pip install pillow
import tkinter
from tkinter import filedialog


root = tkinter.Tk()
root.withdraw()


def export_png(draw, res, path, scaling):
    to_export = []
    for i in range(0, len(draw[0])):
        for _ in range(0, scaling):
            for j in range(0, len(draw)):
                for _ in range(0, scaling):
                    to_export += (draw[j][i][0], draw[j][i][1], draw[j][i][2])

    im = Image.frombytes("RGB", (res[0] * scaling, res[1] * scaling), bytes(to_export))
    im.save(path)


def save_as(name):
    directory = filedialog.asksaveasfilename(initialfile=name)
    return directory


def user_save_png(cont):
    path = save_as(f"{cont['Name']}.png")
    if path:
        export_png(cont['Draw'], cont['CanvasSize'], path, 100)
