import tkinter as tk


COLORS = ['#FF0000', '#00FF00', '#0000FF', '#000000', '#FFFFFF',
          '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


class SelectColor:
    def __init__(self, colors, color_id=0):
        self.colors = colors
        self.new_color_id = color_id=0

    def dialog_color(self, event=None, main=False):
        if main:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel()
        self.window.overrideredirect(True)
        self.window.lift()
        # объект фрейма результатов измерения
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

    def get_color_id(self):
        """ Получение id color после отработки dialog_get_color"""
        return self.new_color_id

    def set_color_id(self, color_id):
        self.new_color_id = color_id


class BoxColor:
    def __init__(self, id_color, obj_color_panel, row, column, color):
        self.id_color = id_color
        self.row = row
        self.column = column
        self.color = color
        self.master = obj_color_panel.window
        self.obj_color_panel = obj_color_panel
        self.box_color = tk.Label(self.master, width=2, background=color,
                anchor='nw')
        self.box_color.grid(row=self.row, column=self.column)
        self.box_color.bind('<Button-1>', lambda event: self.event())

    def event(self):
        # записываю новый цвет 
        self.obj_color_panel.new_color_id = self.id_color
        # и уничтожаю окно
        self.master.destroy()
        self.master.quit()


if __name__ == '__main__':
    color = SelectColor(COLORS)
    color.dialog_color(main=True)
    print(color.get_color_id())
