import tkinter as tk


COLORS = ['#FF0000', '#00FF00', '#0000FF', '#000000', '#FFFFFF',
          '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


class SelectColor:
    def __init__(self, colors, obj_measure_frame=None, event=None, main=False):
        if main:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel()
        self.window.overrideredirect(True)
        #self.window.grid_columnconfigure(0, weight=1)
        #self.window.grid_rowconfigure(0, weight=1)
        self.window.lift()
        #if sys.platform.startswith('win'):
        #    self.window.iconbitmap('mapfract.ico')
        #else:
        #    pass
        self.colors = colors
        # объект фрейма результатов измерения
        self.obj_measure_frame=obj_measure_frame
        row = -1
        self.list_box_color = []
        for i in range(len(self.colors)):
            column = i % 3
            if column == 0:
                row += 1
            box_color = BoxColor(i, self, row, column, self.colors[i])
            self.list_box_color.append(box_color)

        # позиционирую окно
        if event != None:
            x = int(event.x_root)
            y = int(event.y_root)
            self.window.geometry('+{}+{}'.format(x, y))

        self.window.mainloop()


class BoxColor:
    def __init__(self, ident, obj_select_color, row, column, color):
        self.id = ident
        self.obj_select_color = obj_select_color
        self.row = row
        self.column = column
        self.color = color
        self.master = self.obj_select_color.window
        self.box_color = tk.Label(self.master, width=2, background=color,
                anchor='nw')
        self.box_color.grid(row=self.row, column=self.column)
        self.box_color.bind('<Button-1>', lambda event: self.event())

    def event(self):
        color_id = self.id
        # записываю новый цвет 
        if self.obj_select_color.obj_measure_frame != None:
            self.obj_select_color.obj_measure_frame.select_color(color_id)
        else:
            print(color_id)
        # и уничтожаю окно
        self.master.destroy()


if __name__ == '__main__':
    root = SelectColor(colors=COLORS, main=True)
