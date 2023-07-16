'''Simple Tk-based typing test with a predefined dictionary.  Words drawn on a canvas and fly
around, and user must type them before they hit the edge to accumulate a score.
'''
import random, logging
import tkinter as tk
from tkinter import ttk

logging.basicConfig(filename='typing_test.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 250
WORD_MARGIN = 20
MOVE_STEPY = 10
MOVE_STEPX = 25

PATHS = ('uvert', 'dvert', 'lhorz', 'rhorz',
          'urdiag', 'uldiag', 'drdiag','dldiag')
PATH_INITIAL_POS = {
    'uvert': ('x', CANVAS_HEIGHT-WORD_MARGIN), 
    'dvert': ('x', WORD_MARGIN),
    'lhorz': (CANVAS_WIDTH-WORD_MARGIN, 'y'),
    'rhorz': (WORD_MARGIN, 'y'),
    'urdiag': (WORD_MARGIN, CANVAS_HEIGHT-WORD_MARGIN),
    'uldiag': (CANVAS_WIDTH-WORD_MARGIN, CANVAS_HEIGHT-WORD_MARGIN),
    'drdiag': (WORD_MARGIN, WORD_MARGIN),
    'dldiag': (CANVAS_WIDTH-WORD_MARGIN, WORD_MARGIN)
}
PATH_MOV = {
    'uvert': (0, -MOVE_STEPY), 
    'dvert': (0, MOVE_STEPY),
    'lhorz': (-MOVE_STEPX, 0),
    'rhorz': (MOVE_STEPX, 0),
    'urdiag': (MOVE_STEPX, -MOVE_STEPY),
    'uldiag': (-MOVE_STEPX, -MOVE_STEPY),
    'drdiag': (MOVE_STEPX, MOVE_STEPY),
    'dldiag': (-MOVE_STEPX, MOVE_STEPY)
}

COLORS = ['red', 'blue', 'purple', 'cyan', 'black', 'yellow',
           'magenta', 'pink', 'brown']

active_words = {}
next_word = 0

dict_file = open('dictionary.txt')
dict_text = dict_file.read()
wordbase = dict_text.split('\n')
for i in range(len(wordbase)-1):
    wordbase[i] = wordbase[i].lower()

def create_test_base():
    '''Make the blank, base ui for the game and focus entry box'''
    widgets = {'name': 'tkinter_object'}
    main = tk.Frame(root, background='dark gray')
    widgets['main'] = main
    main.grid()

    testcanv = tk.Canvas(main, width=600, height=250, background='dark gray')
    widgets['testcanv'] = testcanv
    testcanv.grid()

    test_entry_string = tk.StringVar()
    testentry = ttk.Entry(main, textvariable=test_entry_string, width=40, background='dark gray')
    widgets['testentry'] = testentry
    testentry.grid()
    testentry.focus_set()

    bottom = tk.Frame(main, width=600, height=50, background='dark gray')
    widgets['bottom'] = bottom
    bottom.grid_propagate(0)
    bottom.grid()

    logging.debug('Board Initialized')

    return widgets

def get_new_word():
    '''Choose a new word, create it on the canvas, and assign it a path'''
    new_word = random.choice(wordbase)
    
    path = random.choice(PATHS)
    if PATH_INITIAL_POS[path][0] == 'x':
        initial_x = random.randint(WORD_MARGIN, CANVAS_WIDTH-WORD_MARGIN)
    else:
        initial_x = PATH_INITIAL_POS[path][0]
    if PATH_INITIAL_POS[path][1] == 'y':
        initial_y = random.randint(WORD_MARGIN, CANVAS_HEIGHT-WORD_MARGIN)
    else:
        initial_y = PATH_INITIAL_POS[path][1]

    widgets['testcanv'].create_text(initial_x, initial_y, text=new_word, 
                                    tags=(new_word, 'word'), 
                                    fill=random.choice(COLORS))
    
    logging.debug(f'{new_word} selected, created at {initial_x},{initial_y} with path {path}')

    active_words[new_word] = (initial_x, initial_y, path)

def word_move():
    '''Move all active words to their next location according to path'''
    global next_word
    
    for word in active_words:
        word_path = active_words[word][2]
        widgets['testcanv'].move(word, PATH_MOV[word_path][0], 
                                PATH_MOV[word_path][1])
        logging.debug(f"Word {word} at {widgets['testcanv'].coords('word')}, count = {next_word}")

    next_word += 1
    if next_word == 10:
        get_new_word()
        next_word = 0

    root.after(200, word_move)
        
    
    # root.after(300, lambda: word_move(new_word))






if __name__ == '__main__':

    root = tk.Tk()
    widgets = create_test_base()
    get_new_word()
    word_move()

    root.mainloop()