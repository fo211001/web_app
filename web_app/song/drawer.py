#-*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import os
from os.path import dirname, join

coordinate = {
    "x": [40, 0],
    0: [-100, 0],
    1: [80, 4],
    2: [220, 4],
    3: [360, 4],
    4: [500, 4]
}

# 1
one = Image.new("RGBA", (50, 35), (0, 0, 0, 0))
draw = ImageDraw.Draw(one)
draw.line((15, 0, 15, 30), fill="black", width=6)
# 2
two = Image.new("RGBA", (50, 35), (0, 0, 0, 0))
draw = ImageDraw.Draw(two)
draw.line((10, 0, 10, 35), fill="black", width=6)
draw.line((25, 0, 25, 35), fill="black", width=6)
# 3
three = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(three)
draw.line((5, 0, 5, 35), fill="black", width=6)
draw.line((15, 0, 15, 35), fill="black", width=6)
draw.line((25, 0, 25, 35), fill="black", width=6)
# 4
four = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(four)
draw.line((2, 0, 2, 35), fill="black", width=6)
draw.line((16, 0, 23, 35), fill="black", width=6)
draw.line((30, 0, 23, 35), fill="black", width=6)
# 5
five = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(five)
draw.line((16, 0, 23, 35), fill="black", width=6)
draw.line((30, 0, 23, 35), fill="black", width=6)
# 6
six = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(six)
draw.line((2, 0, 23, 35), fill="black", width=6)
draw.line((16, 0, 23, 35), fill="black", width=6)
draw.line((30, 0, 30, 35), fill="black", width=6)
# 7
seven = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(seven)
draw.line((2, 0, 9, 35), fill="black", width=6)
draw.line((16, 0, 9, 35), fill="black", width=6)
draw.line((30, 0, 30, 35), fill="black", width=6)
draw.line((40, 0, 40, 35), fill="black", width=6)
# 8
eight = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(eight)
draw.line((2, 0, 9, 35), fill="black", width=6)
draw.line((16, 0, 9, 35), fill="black", width=6)
draw.line((30, 0, 30, 35), fill="black", width=6)
draw.line((38, 0, 38, 35), fill="black", width=6)
draw.line((48, 0, 48, 35), fill="black", width=6)
# 9
nine = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(nine)
draw.line((2, 0, 2, 35), fill="black", width=6)
draw.line((16, 0, 40, 35), fill="black", width=6)
draw.line((40, 0, 16, 35), fill="black", width=6)
# 10
ten = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(six)
draw.line((16, 0, 40, 35), fill="black", width=6)
draw.line((40, 0, 16, 35), fill="black", width=6)
# 11
eleven = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(eleven)
draw.line((2, 0, 30, 35), fill="black", width=6)
draw.line((30, 0, 2, 35), fill="black", width=6)
draw.line((40, 0, 40, 35), fill="black", width=6)
# 12
twelve = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(twelve)
draw.line((2, 0, 30, 35), fill="black", width=6)
draw.line((30, 0, 2, 35), fill="black", width=6)
draw.line((40, 0, 40, 35), fill="black", width=6)
draw.line((45, 0, 45, 35), fill="black", width=6)
# 0
zero = Image.new("RGBA", (50, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(zero)

first_pos = {
    0: zero,
    1: one,
    2: two,
    3: three,
    4: four,
    5: five,
    6: six,
    7: seven,
    8: eight,
    9: nine,
    10: ten,
    11: eleven,
    12: twelve
}

# Рисуем палец
finger = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
draw = ImageDraw.Draw(finger)
draw.ellipse((0, 0, 35, 35), fill="red", outline="red")

# рисуем cross
cross = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
draw = ImageDraw.Draw(cross)
draw.line((0, 0, 35, 35), fill="red", width=7)
draw.line((35, 0, 0, 35), fill="red", width=7)

# 1 струна
struna = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
draw = ImageDraw.Draw(struna)
draw.line((20, 0, 20, 35), fill="black", width=5)


# создаем апликатуру
def image_fingering(fingering):
    # позиция
    path = join(dirname(dirname(__file__)), "images")
    fingering = [int(x) if x != 'x' else 'x' for x in fingering]
    posicion = first_pos[min(fingering)]
    draw = ImageDraw.Draw(posicion)
    # рисуем гриф гитары
    griff = Image.open(join(path, "Grif.png"), "r")
    draw = ImageDraw.Draw(griff)
    # рисуем струну
    draw.bitmap((0, 205), struna, fill="black")
    fingering = list(fingering)
    # рисуем апликатуру
    for i, lad in enumerate(fingering):
        if lad == "x":
            draw.bitmap((coordinate["x"][0], 203.5 - i * 41.5), cross, fill="red")
        # elif lad == 0:
        #     x = coordinate[lad][0]
        #     y = coordinate[lad][1] + 203.5 - i * 41.5
        #     draw.bitmap((x, y), finger, fill="red")
        # else:
        if min(fingering) != 0:
            lad -= (min(fingering) - 1)
        x = coordinate[lad][0]
        y = coordinate[lad][1] + 203.5 - i * 41.5
        draw.bitmap((x, y), finger, fill="red")

    puth = join(path, ",".join(unicode(z) for z in fingering) + ".png")
    # рисуем лад
    draw.bitmap((75, 246), posicion, fill="black")
    # сохраняем
    griff.save(puth)
    # puth = "images" + ",".join(unicode(z) for z in fingering) + ".png"
    # griff.save(puth)
    del draw
    return puth


