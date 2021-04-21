from Goulib.image import *
from pynput.mouse import Button, Controller, Listener
from time import sleep
import math_2 as mt
import base64

garticcolor = Gcolors.Palette([Gcolors.Color("#000000"), Gcolors.Color("#666666"), Gcolors.Color("#0050CD"), Gcolors.Color("#FFFFFF"), Gcolors.Color("#AAAAAA"), Gcolors.Color("#26C9FF"), Gcolors.Color("#017420"), Gcolors.Color("#691506"), Gcolors.Color(
    "#964112"), Gcolors.Color("#11B03C"), Gcolors.Color("#FF0013"), Gcolors.Color("#FF7829"), Gcolors.Color("#B0701C"), Gcolors.Color("#99004E"), Gcolors.Color("#CB5A57"), Gcolors.Color("#FFC126"), Gcolors.Color("#FF008F"), Gcolors.Color("#FEAFA8")])

coord = ((362, 322), (407, 321), (442, 323), (369, 360), (406, 359), (441, 354), (361, 399), (404, 398), (434, 398),
         (368, 435), (409, 434), (437, 434), (370, 469), (398, 469), (443, 471), (366, 509), (406, 514), (439, 514))


garticcolorcoord = {x: y for x, y in zip(garticcolor, coord)}

click1 = False
click2 = False
mouse = Controller()

coordspen = [(526, 734), (580, 739)]


class DecodeImageError(Exception):
    pass


def on_click(x, y, button, pressed):
    global click1, click2, mouse
    if pressed:
        if not click1:
            click1 = mouse.position
        elif not click2:
            click2 = mouse.position
        else:
            return False


def get_size():
    global click1, click2
    listener = Listener(on_click=on_click)
    listener.start()
    while not click1:
        pass
    while not click2:
        pass
    listener.stop()
    return (click2[1] - click1[1], click2[0] - click1[0]), click1


def change_color(pixel):
    global mouse, garticcolorcoord
    position = mouse.position
    mouse.position = garticcolorcoord[pixel]
    mouse.click(Button.left)
    mouse.position = position


def change_pen(number):
    global mouse, coordspen
    position = mouse.position
    mouse.position = coordspen[number]
    mouse.click(Button.left)
    mouse.position = position


def draw(image, start, pen):
    global mouse, garticcolorcoord
    mouse.position = start
    size = image.size
    pixel = image.getpixel((0, 0))
    change_color(pixel)
    mouse.press(Button.left)
    lastpixel = pixel
    position = mouse.position
    change_pen(pen)
    add = [1, 5][pen]  # Size of the pen

    for x in range(0, size[1], add):
        lastpixel = image.getpixel((0, x))
        pixel = lastpixel
        if pixel != 3:
            change_color(pixel)
            mouse.press(Button.left)
        for y in range(0, size[0], add):
            pixel = image.getpixel((y, x))
            if lastpixel == pixel:
                position = (position[0], position[1] + add)
            else:
                lastpixel = pixel
                mouse.position = position
                sleep(0.008)
                mouse.release(Button.left)
                mouse.move(0, add)
                position = mouse.position
                if pixel != 3:
                    change_color(pixel)
                    mouse.press(Button.left)

        mouse.position = position
        sleep(0.008)
        mouse.release(Button.left)
        mouse.position = (mouse.position[0] + add, start[1])
        position = mouse.position
    mouse.release(Button.left)


def decode(url):
    try:
        return Image(url)  # Path or Url
    except FileNotFoundError:
        if url[:22] == r"data:image/png;base64,":  # PNG in base 64
            return Image(url[22:])
        if url[:23] == r"data:image/jpeg;base64,":  # JPEG in base 64
            data = base64.b64decode(url[22:])
            with open(r"data\garticphone.jpg", "wb") as file:
                file.write(data)
            return Image("garticphone.jpg")
        else:
            raise DecodeImageError("'%s' cannot be decoded" % (
                url if len(url) < 15 else url[:15] + "..."))


def main():
    global garticcolor, garticcolorcoord

    url = input("Url de l'image:")
    image = decode(url)

    print("0: Trés précis")
    print("1: Plutot précis")
    pen = int(input())

    print("2eme partie")
    size = image.size
    size2, start = get_size()
    coef = min(size2[0] / size[0], size2[1] / size[1])
    size2 = (mt.rint(coef * size[0]), mt.rint(coef * size[1]))

    image = image.resize(reversed(size2))
    image = image.convert("P", colors=garticcolor)
    print("Go!!")
    sleep(3)
    draw(image, start, pen)


if __name__ == "__main__":
    main()
