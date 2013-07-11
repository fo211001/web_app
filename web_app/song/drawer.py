#-*- coding: utf-8 -*-
from PIL import Image, ImageDraw

coordinate = {
    "x": [0, 0],
    0: [-100, 0],
    1: [70, 4],
    2: [210, 4],
    3: [350, 4],
    4: [490, 4]
}
first_pos = {
    1: "1.png",
    2: "2.png",
    3: "3.png",
    4: "4.png",
    5: "5.png",
    6: "6.png",
    7: "7.png",
    8: "8.png",
    9: "9.png",
    10: "10.png",
    11: "11.png",
    12: "12.png"
}


# создаем апликатуру
def image_fingering(spisok):
    # Рисуем палец
    finger = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
    draw = ImageDraw.Draw(finger)
    draw.ellipse((0, 0, 35, 35), fill="red", outline="red")

    # рисуем бэре
    bere = Image.new("RGBA", (75, 245), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bere)
    draw.ellipse((25, 0, 50, 245), fill="red", outline="red")

    # рисуем cross
    cross = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
    draw = ImageDraw.Draw(cross)
    draw.line((0, 0, 35, 35), fill="red", width=7)
    draw.line((35, 0, 0, 35), fill="red", width=7)

    # рисуем лад
    min_lad = min(spisok)
    posicion = Image.open(first_pos[min_lad])
    draw = ImageDraw.Draw(posicion)
    aplic = Image.open("Grif.png")
    draw = ImageDraw.Draw(aplic)
    spisok = list(spisok)


    for i, lad in enumerate(spisok):
        lad -= (min_lad - 1)
        x = coordinate[lad][0]
        y = coordinate[lad][1] + 203.5 - i * 41.5
        if lad == 'x':
            draw.bitmap((x, y), cross, fill="red")
        else:
            draw.bitmap((x, y), finger, fill="red")
        aplic.save("image_fingering.png", "PNG")
    del draw


