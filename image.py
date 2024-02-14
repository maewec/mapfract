"""
Пакет для получения информации из изображения
"""

from PIL import Image, ImageDraw, ImageTk


class ImagePIL:
    """Работа с изображением"""
    
    def __init__(self, path_image):
        self.image = Image.open(path_image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]

    def get_tk_image(self):
        return ImageTk.PhotoImage(self.image)

    def savefile(self, newfile, result):
        # сохранение изображения со всеми нарисованными на канвасе элементами
        # список линий для отображения
        list_result = result.list_result
        savimage = self.image.copy()
        draw = ImageDraw.Draw(savimage)
        # последовательно обхожу список и рисую активные линии
        for res in list_result:
            line = res.line
            if line.key_visible:
                x = line.x
                y = line.y
                x1 = line.x1
                y1 = line.y1
                color = line.color
                width = line.width

                draw.line((x, y, x1, y1), fill=color, width=width)

        savimage.save(newfile)
