'''Simple Tk-based typing test with a predefined dictionary.  Words drawn on a canvas and fly
around, and user must type them before they hit the edge to accumulate a score.
'''
import random, logging
import tkinter as tk
from tkinter import ttk

logging.basicConfig(filename='typing_test.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

dict_file = open('dictionary.txt')
dict_text = dict_file.read()
wordbase = dict_text.split('\n')

def create_test_base():
    '''Make the blank, base ui for the game and focus entry box'''
    widgets = {'name': 'tkinter_object'}
    main = ttk.Frame(root)
    widgets['main'] = main
    main.grid()

    testcanv = tk.Canvas(main, width=600, height=250)
    widgets['testcanv'] = testcanv
    testcanv.grid()

    test_entry_string = tk.StringVar()
    testentry = ttk.Entry(main, textvariable=test_entry_string, width=40)
    widgets['testentry'] = testentry
    testentry.grid()
    testentry.focus_set()

    bottom = ttk.Frame(main, width=600, height=50)
    widgets['bottom'] = bottom
    bottom.grid_propagate(0)
    bottom.grid()

    return widgets

def get_new_word():
    new_word = random.choice(wordbase)
    logging.debug(f'{new_word} selected')
    initial_x = 100
    initial_y = 200
    widgets['testcanv'].create_text(initial_x, initial_y, text=new_word, tags=new_word)
    return {new_word: (initial_x, initial_y)}

def word_draw_traject(new_word, initial_x, initial_y):
    '''Choose a word from wordbase, draw it on canvas, and set it on a path'''
    paths = ['uvert', 'dvert', 'lhorz', 'rhorz', 'udiag', 'ddiag'] # up vertical, left horizontal
    
    widgets['testcanv'].move(new_word, 20, -20)
    root.after(300, lambda: word_draw_traject(new_word))





if __name__ == '__main__':

    root = tk.Tk()
    widgets = create_test_base()
    new_word = get_new_word()
    word_draw_traject(new_word)
    root.mainloop()