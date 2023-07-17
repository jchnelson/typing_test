'''Simple Tk-based typing test with a predefined dictionary.  Words appear and move, 
and user must type them before they hit the edge to accumulate a score.
'''
import random, logging
import tkinter as tk
from tkinter import messagebox

logging.basicConfig(filename='typing_test.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s: %(message)s')
logging.disable(logging.DEBUG)

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 250
WORD_MARGIN = 20
MOVE_STEPY = 10
MOVE_STEPX = 25
X_ADJUST = 20

#up-vertical, left-horizontal, down-right-diagonal, etc
PATHS = ('uvert', 'dvert', 'lhorz', 'rhorz',
          'urdiag', 'uldiag', 'drdiag','dldiag')

#establish acceptable area for word to appear
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

#make indices for direction of movement
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
player_score = 0
gamespeed = 400
score_barrier = 100
interval = 10

dict_file = open('dictionary.txt')
dict_text = dict_file.read()
wordbase = dict_text.split('\n')
for i in range(len(wordbase)-1):
    wordbase[i] = wordbase[i].lower()

class TypingBoard():
    def __init__(self):
        self.main = tk.Frame(root, background='dark gray')
        self.main.grid()

        self.testcanv = tk.Canvas(self.main, width=600, height=250, background='dark gray')
        self.testcanv.grid()

        self.testentry = tk.Entry(self.main, width=40,
                            highlightthickness=3)

        self.testentry.grid()
        self.testentry.bind('<Return>', lambda e: check_entry(e, self))
        self.testentry.bind('<BackSpace>', lambda e: clear_color(e, self))

        self.bottom = tk.Frame(self.main, width=600, height=50, background='dark gray')
        self.bottom.grid_propagate(0)
        self.bottom.grid_columnconfigure(0, weight=1)
        self.bottom.grid()
        
        self.bottom_text = tk.Label(self.bottom, text='Score: 0\nSpeed up at 100',
                                    font=('arial', 13, 'bold'), background='dark gray')
        logging.info(f"StringVar for bottom_text initialized as {repr(self.bottom_text['text'])}")
        self.bottom_text.grid(sticky='e')

    logging.debug('Board Initialized')


def check_entry(event, typingboard):
    '''Check text from entry box against active words, remove them from canvas
     if matched. Handle color changes and score adjustment.'''
    global player_score, score_barrier, gamespeed
    entry_string = typingboard.testentry.get()
    logging.info(f'Checking entry string... current value {repr(entry_string)}')
    word_list = list(active_words.keys())

    if entry_string in word_list:
        typingboard.testcanv.delete(typingboard.testcanv.find_withtag(entry_string)[0])
        player_score += len(entry_string)
        typingboard.bottom_text['text'] = (f'Score: {player_score}\nSpeed up at {score_barrier}')
        typingboard.testentry.delete(0, 'end')
        typingboard.testentry['highlightcolor']= 'SystemWindowFrame'
        if player_score >= score_barrier:
            score_barrier += 100
            gamespeed -= 50

    else:
        typingboard.testentry['highlightcolor'] = 'red'
    
def clear_color(event, typingboard):
    '''Remove red border of entry box when player is correcting mistake'''
    typingboard.testentry['highlightcolor'] = 'SystemWindowFrame'


def get_new_word(typingboard):
    '''Choose a new word, create it on the canvas, and assign it a path'''
    new_word = random.choice(wordbase)
    
    path = random.choice(PATHS)
    if PATH_INITIAL_POS[path][0] == 'x':
        initial_x = random.randint(WORD_MARGIN+X_ADJUST, 
                                   CANVAS_WIDTH-WORD_MARGIN-X_ADJUST)
    else:
        initial_x = PATH_INITIAL_POS[path][0]
    if PATH_INITIAL_POS[path][1] == 'y':
        initial_y = random.randint(WORD_MARGIN, CANVAS_HEIGHT-WORD_MARGIN)
    else:
        initial_y = PATH_INITIAL_POS[path][1]

    typingboard.testcanv.create_text(initial_x, initial_y, text=new_word, 
                                    tags=(new_word, 'word'), font=('arial', 13, 'bold'), 
                                    fill=random.choice(COLORS))
    
    logging.debug(f'{new_word} selected, created at {initial_x},{initial_y} with path {path}')

    active_words[new_word] = (initial_x, initial_y, path)

def word_move(typingboard):
    '''Move all active words to their next location according to path'''
    global next_word, gameover

    for word in active_words:
        word_path = active_words[word][2]
        typingboard.testcanv.move(word, PATH_MOV[word_path][0], 
                                PATH_MOV[word_path][1])
        
        logging.debug(f"Word {word} at {typingboard.testcanv.coords(word)}, count = {next_word}")
        logging.debug(f"Word {word}, coords type \
{type(typingboard.testcanv.coords(word))} len {len(typingboard.testcanv.coords(word))}")

        if len(typingboard.testcanv.coords(word)) > 0:
            logging.debug(f"word {word} at x{typingboard.testcanv.coords(word)[0]},\
 y{typingboard.testcanv.coords(word)[0]}")
            if not (0 < typingboard.testcanv.coords(word)[0] < 600) or \
            not (0 < typingboard.testcanv.coords(word)[1] < 250):
                messagebox.showinfo('Defeat!', f'Final Score {player_score}')
                root.destroy()

    next_word += 1
    if next_word == interval:
        get_new_word(typingboard)
        next_word = 0
    root.after(gamespeed, lambda: word_move(typingboard))


if __name__ == '__main__':
    messagebox.showinfo('Typing Test', 'Welcome to the Typing Test game!\nEnter the words as quickly as you can, and\nhit return. Go for a high score!')
    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    root.after(1, lambda: root.focus_force())
    tboard = TypingBoard()
    root.after(10, lambda: tboard.testentry.focus_set())
    get_new_word(tboard)
    word_move(tboard)
    root.mainloop()