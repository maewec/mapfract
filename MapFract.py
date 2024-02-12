import sys, os

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
            #image_frame.set_coords()
            #image_frame.unlock()
        except Exception as e:
            mb.showerror('Ошибка', f'Не удалось открыть файл\n{e}')


class Toolbar:
    def __init__(self, master, row, column):
        pass


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

image_frame = ImageFrame(root, 0, 0)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()
