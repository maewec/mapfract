import tkinter.messagebox as mb

text = '''Программа предназначена для измерения длины отрезков
на фотографиях в пикселях и в единицах длины.

        Автор: Немцев Д.'''

title = 'О программе'

def about():
    mb.showinfo(title, text)
