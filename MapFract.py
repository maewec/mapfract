import sys, os

import math

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from PIL import ImageTk

import image


title_name = 'Map Fracture'

root = tk. Tk()
root.title(title_name)

#if sys.platform.startswith('win'):
#    root.iconbitmap('mapfract.ico')
#else:
#    pass

global img

def loadfile():
    file_name = fd.askopenfilename()
    global path, short_file_name, short_file_wo_ext
    if os.path.isfile(file_name):
        path, short_file_name = os.path.split(file_name)
        short_file_wo_ext = os.path.splitext(short_file_name)[0]
        root.title('{} - {}'.format(short_file_name, title_name))
        global img
        try:
            img = image.ImagePIL(file_name)
            # отображение изображения
            image_frame.reload_image()
            #image_frame.unlock()
        except Exception as e:
            mb.showerror('Ошибка', f'Не удалось открыть файл\n{e}')


class Toolbar:
    def __init__(self, master, row, column, image_frame):
        # фрейм с изображением
        self.imgf = image_frame
        # отступ по умолчанию
        padx = 2
        pady = 2
        # список координат для измерений
        self.list_points_measure = []

        self.frame = tk.Frame(master)
        self.frame.grid(row=row, column=column, sticky='nw',
                        padx=padx, pady=pady)

        # Фрейм информации
        self.frame_info = tk.LabelFrame(self.frame, text='Информация')
        self.frame_info.grid(row=0, column=0, sticky='nw',
                             padx=padx, pady=pady)
        self.text_info = 'x={}\ny={}'
        self.label_info = tk.Label(self.frame_info, text=self.text_info.format(0, 0))
        self.label_info.grid(row=0, column=0)
        # забиндить отображение координат на изображении
        self.canv_bind_info_coord = self.imgf.canv.bind('<Motion>', self.info_coord,
                                                        add=True)
        self.label_info_len = tk.Label(self.frame_info, text='')
        self.label_info_len.grid(row=1, column=0)
        
        # Фрейм масштаба
        self.frame_scale = tk.LabelFrame(self.frame, text='Масштаб')
        self.frame_scale.grid(row=0, column=1, sticky='nsw',
                              padx=padx, pady=pady)
        # поле ввода количества пикселей
        self.entry_scale_pixels = tk.Entry(self.frame_scale, width=8)
        self.entry_scale_pixels.insert(0, 1)
        self.entry_scale_pixels.grid(row=0, column=0)
        tk.Label(self.frame_scale, text='px').grid(row=0, column=1)
        # поле ввода единиц длины
        self.entry_scale_len = tk.Entry(self.frame_scale, width=8)
        self.entry_scale_len.insert(0, 1)
        self.entry_scale_len.grid(row=1, column=0)
        tk.Label(self.frame_scale, text='').grid(row=1, column=1)
        # кнопка определения числа пикселей
        self.button_scale_pixels = tk.Button(self.frame_scale, text='Измерить шкалу')
        self.button_scale_pixels.bind('<Button-1>',
                                      lambda event: self.measure('scale'))
        self.button_scale_pixels.grid(row=2, column=0, columnspan=2,
                                      sticky='nwe')
        # вывод перевода пикселей в длину
        self.label_scale = tk.Label(self.frame_scale)
        self.label_scale.grid(row=3, column=0, columnspan=2)

    def info_coord(self, event):
        # при скроллинге канваса правильное отображение координат
        x = int(self.imgf.canv.canvasx(event.x))
        y = int(self.imgf.canv.canvasy(event.y))
        self.label_info.configure(text=self.text_info.format(x, y))

    def measure(self, type_measure):
        self.canv_bind_measure = self.imgf.canv.bind('<Button-1>',
                         lambda event: self.click_measure(event, type_measure),
                         add=True)

    def click_measure(self, event, type_measure):
        if len(self.list_points_measure) == 0:
            x = self.imgf.canv.canvasx(event.x)
            y = self.imgf.canv.canvasy(event.y)
            self.list_points_measure.append([x, y])
            self.line = self.imgf.canv.create_line(x, y, x+1, y+1,
                                              fill='red', width=3)
            self.canv_bind_line = self.imgf.canv.bind('<Motion>',
                        lambda event: self.draw_line(event, x, y, type_measure),
                                     add=True)
        elif len(self.list_points_measure) == 1:
            self.imgf.canv.unbind('<Motion>', self.canv_bind_line)
            # снова включаю отображение координат (отключаются после unbind)
            self.canv_bind_info_coord = self.imgf.canv.bind('<Motion>', self.info_coord,
                                                   add=True)
            if type_measure != 'draw_distance':
                self.imgf.canv.delete(self.line)
            x = self.imgf.canv.canvasx(event.x)
            y = self.imgf.canv.canvasy(event.y)
            self.list_points_measure.append([x, y])
            if type_measure != 'draw_distance':
                self.set_measure(type_measure)
            # отвязываем функцию и обнуляем список
            self.imgf.canv.unbind('<Button-1>', self.canv_bind_measure)
            self.list_points_measure = []
        else:
            raise ('Не может быть третьего клика для горизонта')

    def set_measure(self, type_measure):
        if len(self.list_points_measure) != 2:
            raise ('Нет списка горизонта для вычисления угла')
        x1, y1 = self.list_points_measure[0]
        x2, y2 = self.list_points_measure[1]
        if type_measure == 'horizont':
            atan = math.atan((y2-y1)/(x2-x1))
            angle = math.degrees(atan)
            # забиваем в поле ввода
            self.entry_rotate_angle.delete(0, 'end')
            self.entry_rotate_angle.insert(0, '{:6.2f}'.format(angle))
        elif type_measure == 'scale':
            l = math.sqrt((x2-x1)**2+(y2-y1)**2)
            l = round(l)
            # забиваем в поле ввода
            self.entry_scale_pixels.delete(0, 'end')
            self.entry_scale_pixels.insert(0, l)
            self.get_multiplier()
        else:
            raise KeyError(f'Ключ {type_measure} не поддерживается')

    def draw_line(self, event, x, y, type_measure):
        x1 = self.imgf.canv.canvasx(event.x)
        y1 = self.imgf.canv.canvasy(event.y)
        self.imgf.canv.coords(self.line, (x, y, x1, y1))
        px = math.sqrt((x-x1)**2+(y-y1)**2)
        if type_measure == 'draw_distance':
            multiplier = self.get_multiplier()
            l = px*multiplier
            text = '{:5.0f} px\n{:5.2e} ед.дл.'.format(px, l)
            self.label_info_len.configure(text=text)
        elif type_measure == 'scale':
            text = '{:5.0f} px'.format(px)
            self.label_info_len.configure(text=text)

    def get_multiplier(self):
        pixels = int(self.entry_scale_pixels.get())
        length = float(self.entry_scale_len.get())
        multiplier = length / pixels
        self.label_scale.configure(text=f'1 px = {multiplier:5.2e}')
        return multiplier

class ImageFrame:
    def __init__(self, master, row, column):
        self.frame = tk.Frame(master)
        self.frame.grid(row=row, column=column, sticky='nw',
                        padx=3, pady=3)
        self.canv = tk.Canvas(self.frame)
        self.canv.grid(row=0, column=0, sticky='nswe')
        self.vscroll = tk.Scrollbar(self.frame, command=self.canv.yview)
        self.hscroll = tk.Scrollbar(self.frame, command=self.canv.xview, orient='horizontal')
        self.vscroll.grid(row=0, column=1, sticky='ns')
        self.hscroll.grid(row=1, column=0, sticky='we')
        self.canv.config(yscrollcommand=self.vscroll.set)
        self.canv.config(xscrollcommand=self.hscroll.set)

        self.frame.grid_rowconfigure(0, weight=1)   # Не скрывать
        self.frame.grid_columnconfigure(0, weight=1)  # не скрывается нижний сайдбар

    def reload_image(self):
        global img
        # надо обязательно сделать полем, иначе уничтожится сборщиком мусора и
        # не будет видно
        self.image_tkinter = img.get_tk_image()
        # задаем размер холста
        self.canv.config(width=img.width, height=img.height)
        # задаем размер холста при прокрутке
        self.canv.config(scrollregion=(0, 0, img.width, img.height))

        self.sprite = self.canv.create_image(0, 0, anchor='nw',
                                             image=self.image_tkinter)


mainmenu = tk.Menu(root)
root.config(menu=mainmenu)
mainmenu.add_command(label='Открыть изображение', command=loadfile)

image_frame = ImageFrame(root, 1, 0)
toolbar     =    Toolbar(root, 0, 0, image_frame=image_frame)

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
