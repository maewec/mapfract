import sys, os

import math

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from PIL import ImageTk

import image, color_panel


title_name = 'Map Fracture'

root = tk. Tk()
root.title(title_name)

#if sys.platform.startswith('win'):
#    root.iconbitmap('mapfract.ico')
#else:
#    pass

global img

COLORS = ['#FF0000', '#00FF00', '#0000FF', '#000000', '#FFFFFF',
          '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

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
    def __init__(self, master, row, column, columnspan, 
                 image_frame, result):
        # фрейм с изображением
        self.imgf = image_frame
        # фрейм с результатами
        self.result = result
        # отступ по умолчанию
        padx = 2
        pady = 2
        # список координат для измерений
        self.list_points_measure = []

        self.frame = tk.Frame(master)
        self.frame.grid(row=row, column=column, columnspan=columnspan, sticky='nw',
                        padx=padx, pady=pady)

        ##################
        # Фрейм информации
        self.frame_info = tk.LabelFrame(self.frame, text='Информация')
        self.frame_info.grid(row=0, column=0, sticky='nsw',
                             padx=padx, pady=pady)
        self.text_info = 'x={}\ny={}'
        self.label_info = tk.Label(self.frame_info, text=self.text_info.format(0, 0),
                anchor='w')
        self.label_info.grid(row=0, column=0, sticky='nw')
        # забиндить отображение координат на изображении
        self.canv_bind_info_coord = self.imgf.canv.bind('<Motion>', self.info_coord,
                                                        add=True)
        self.label_info_len = tk.Label(self.frame_info, text='', anchor='w')
        self.label_info_len.grid(row=1, column=0, sticky='nw')
        
        ################
        # Фрейм масштаба
        self.frame_scale = tk.LabelFrame(self.frame, text='Масштаб')
        self.frame_scale.grid(row=0, column=1, sticky='nsw',
                              padx=padx, pady=pady)
        # поле ввода количества пикселей
        self.entry_scale_pixels = tk.Entry(self.frame_scale, width=8)
        self.entry_scale_pixels.insert(0, 1)
        self.entry_scale_pixels.bind('<Return>', lambda event: self.get_multiplier())
        self.entry_scale_pixels.grid(row=0, column=0)
        tk.Label(self.frame_scale, text='px', anchor='w').grid(row=0, column=1)
        # поле ввода единиц длины
        self.entry_scale_len = tk.Entry(self.frame_scale, width=8)
        self.entry_scale_len.insert(0, 1)
        self.entry_scale_len.bind('<Return>', lambda event: self.get_multiplier())
        self.entry_scale_len.grid(row=1, column=0)
        tk.Label(self.frame_scale, text='', anchor='w').grid(row=1, column=1)
        # кнопка определения числа пикселей
        self.button_scale_pixels = tk.Button(self.frame_scale, text='Измерить шкалу')
        self.button_scale_pixels.bind('<Button-1>',
                                      lambda event: self.measure('scale'))
        self.button_scale_pixels.grid(row=2, column=0, columnspan=2,
                                      sticky='nwe')
        # вывод перевода пикселей в длину
        self.label_scale = tk.Label(self.frame_scale, anchor='w')
        self.label_scale.grid(row=3, column=0, columnspan=2)

        #################
        # Фрейм измерений
        self.frame_measure = tk.LabelFrame(self.frame, text='Измерения')
        self.frame_measure.grid(row=0, column=2, sticky='nsw',
                              padx=padx, pady=pady)
        self.button_measure_line = tk.Button(self.frame_measure, text='Измерить длину')
        self.button_measure_line.bind('<Button-1>',
                                      lambda event: self.measure('draw_distance'))
        self.button_measure_line.grid(row=0, column=0, sticky='nw')

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
            # создание линии
            self.line = self.imgf.canv.create_line(x, y, x+1, y+1,
                                              fill=COLORS[0], width=3)
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
        else:
            px = math.sqrt((x2-x1)**2+(y2-y1)**2)
            px = round(px)
            multiplier = self.get_multiplier()
            length = px*multiplier
            if type_measure == 'scale':
                # забиваем в поле ввода
                self.entry_scale_pixels.delete(0, 'end')
                self.entry_scale_pixels.insert(0, px)
            elif type_measure == 'draw_distance':
                # переношу результаты в поле результатов
                self.result.add_result(length, px, self.line)
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
            text = '{:.0f} px\n{:.4f}'.format(px, l)
            # переношу результаты в поле информации
            self.label_info_len.configure(text=text)
        elif type_measure == 'scale':
            text = '{:.0f} px'.format(px)
            self.label_info_len.configure(text=text)

    def get_multiplier(self):
        pixels = int(self.entry_scale_pixels.get())
        length = float(self.entry_scale_len.get())
        multiplier = length / pixels
        self.label_scale.configure(text=f'1 px = {multiplier:.4f}')
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


class ResultFrame:
    def __init__(self, master, row, column):
        # список всех фреймов с результатами
        self.list_result = []
        self.frame = tk.Frame(master)
        self.frame.grid(row=row, column=column, sticky='nw',
                        padx=3, pady=3)

        self.frame_result = tk.LabelFrame(self.frame, text='Результаты')
        self.frame_result.grid(row=0, column=0, sticky='nw',
                               padx=2, pady=3)
        tk.Label(self.frame_result, text='N, check, length', anchor='w').grid(row=0, column=0)

    def add_result(self, length, pixel, line):
        res = MeasureFrame(length, pixel, line, self.frame_result)
        res.draw()
        self.list_result.append(res)


class MeasureFrame:
    count = 1
    def __init__(self, length, pixel, line, master):
        self.id = MeasureFrame.count
        MeasureFrame.count += 1
        self.length = length
        self.pixel = pixel
        self.line = line
        self.master = master
        self.color_id = 0
        self.color_var = tk.StringVar(value=COLORS[self.color_id])
        self.view_length_var = tk.StringVar(value=self.view_length[0])
        self.var_visible = tk.BooleanVar()

    view_length = ['Длина', 'px', 'Нет']

    def draw(self):
        self.row = tk.Frame(self.master)
        self.row.grid(row=self.id, column=0)
        # номер результата
        self.label_num = tk.Label(self.row, text='{:2.0f}'.format(self.id))
        self.label_num.grid(row=0, column=0)
        # Чекбокс видимости
        self.var_visible.set(True)
        self.check_visible = tk.Checkbutton(self.row, text='',
                variable=self.var_visible, onvalue=True, offvalue=False)
        self.check_visible.grid(row=0, column=1)
        # Текст с длиной
        self.text_length = tk.Text(self.row, width=10, height=1, wrap='none', bg='#cccccc')
        self.text_length.grid(row=0, column=2)
        self.text_length.insert(1.0, '{:.4f}'.format(self.length))
        self.text_length.configure(state='disabled')
        # Текст с пикселями
        self.text_px = tk.Text(self.row, width=5, height=1, wrap='none', bg='#cccccc')
        self.text_px.grid(row=0, column=3)
        self.text_px.insert(1.0, '{:.0f}'.format(self.pixel))
        self.text_px.configure(state='disabled')
        # Цвет
        self.label_color = tk.Label(self.row, width=2, background=COLORS[self.color_id])
        self.label_color.grid(row=0, column=4)
        self.label_color.bind('<Button-1>', lambda event: color_panel.SelectColor(COLORS, self, event))
        # Отображение размера на полотне
        self.combobox_length = ttk.Combobox(self.row, textvariable=self.view_length_var,
                values=self.view_length, width=4, state='readonly')
        self.combobox_length.grid(row=0, column=5)

    def select_color(self, color_id):
        self.color_id = color_id
        self.label_color.configure(background=COLORS[self.color_id])
        # обращаюсь к глобальной переменной холста
        image_frame.canv.itemconfig(self.line, fill=COLORS[self.color_id])


mainmenu = tk.Menu(root)
root.config(menu=mainmenu)
mainmenu.add_command(label='Открыть изображение', command=loadfile)

result      = ResultFrame(root, 1, 0)
image_frame =  ImageFrame(root, 1, 1)
toolbar     =     Toolbar(root, 0, 0, columnspan=2, 
                          image_frame=image_frame, result=result)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
