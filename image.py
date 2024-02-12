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
