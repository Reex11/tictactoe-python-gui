from tkinter import *
from tkinter.messagebox import *
import random
from threading import Timer

"""
BOARD SHAPE

7 | 8 | 9
4 | 5 | 6
1 | 2 | 3

"""

game_mode = None  # 'PvC' Player vs Computer or 'PvP' Player vs Player
p1_symbol = None  # 'X' or 'O'

lose_messages = ["Game Over v_v", "Looks like computers are better than human :)",
                 "You lost, but you can try again.", "Don't cry.. its just a game.",
                 "This is only the beginning.. AI will dominate!", "GAME OVER", "You lost :("]

win_messages = ["Congratulations, You Won!", "You are the best!", "You are the winner!",
                "Give me a chance :'(", "You won this time, but I will win next time!"]


def board_check(board):  # board is a dictionary
    # if the board is full

    if board[1] == board[2] == board[3] == 'X' or \
            board[4] == board[5] == board[6] == 'X' or \
            board[7] == board[8] == board[9] == 'X' or \
            board[1] == board[4] == board[7] == 'X' or \
            board[2] == board[5] == board[8] == 'X' or \
            board[3] == board[6] == board[9] == 'X' or \
            board[1] == board[5] == board[9] == 'X' or \
            board[3] == board[5] == board[7] == 'X':
        return 'X_win'
    # if O wins
    elif board[1] == board[2] == board[3] == 'O' or \
            board[4] == board[5] == board[6] == 'O' or \
            board[7] == board[8] == board[9] == 'O' or \
            board[1] == board[4] == board[7] == 'O' or \
            board[2] == board[5] == board[8] == 'O' or \
            board[3] == board[6] == board[9] == 'O' or \
            board[1] == board[5] == board[9] == 'O' or \
            board[3] == board[5] == board[7] == 'O':
        return 'O_win'
    elif sum(value == ' ' for value in board.values()) == 0:
        return 'draw'
    # if X wins


def ChooseSymbolScreen():
    global p1_symbol
    screen = Tk()
    txt_playersymbol = StringVar()
    screen.title("Choose Symbol")
    screen.geometry("300x300")
    Label(screen, text="Choose P1 symbol:").pack(pady=(30, 0))

    # add button to screen with padding
    Button(screen, height=2, text="X", command=lambda: SymbolCallBack("X", screen)
           ).pack(pady=(10, 0), fill=X)
    Button(screen, height=2, text="O", command=lambda: SymbolCallBack("O", screen)
           ).pack(pady=(0, 10), fill=X)

    root.mainloop()


def SymbolCallBack(symbol, screen):
    global p1_symbol
    # playersymbol.set(symbol)
    p1_symbol = symbol
    screen.destroy()


def loadMainMenu():
    global root, gamemode
    root = Tk()
    gamemode = StringVar()
    root.title("Main Menu")
    root.geometry("300x300")
    l1 = Label(root, text="Welcome to Tic Tac Toe")
    l1.pack(pady=10)

    Label(root, text="Choose the Game mode:").pack(pady=(30, 0))

    # add button to root with padding
    Button(root, height=2, text="Player vs Computer", command=lambda: GameModeCallBack("PvC")
           ).pack(pady=(10, 0), fill=X)
    Button(root, height=2, text="Player vs Player", command=lambda: GameModeCallBack("PvP")
           ).pack(pady=(0, 10), fill=X)

    closebtn = Button(root, text="Exit", command=lambda: root.destroy())
    closebtn.pack(side=BOTTOM, fill=X, padx=10, pady=10)

    root.mainloop()


def GameModeCallBack(mode):
    global game_mode, p1_symbol
    game_mode = mode
    root.destroy()

    ChooseSymbolScreen()

    GameScreen()

    loadMainMenu()


class GameScreen:
    def __init__(self):

        self.board = {7: ' ', 8: ' ', 9: ' ', 4: ' ',
                      5: ' ', 6: ' ', 1: ' ', 2: ' ', 3: ' '}
        self.game_status = 'X_turn'

        self.root = Tk()
        self.root.title("Game")
        self.root.geometry("300x300")
        Label(self.root, text=game_mode, fg="grey").pack(pady=10)
        self.turnlabel = Label(self.root,wraplength=300)
        self.turnlabel.pack(pady=10)
        self.gscreen = Frame(self.root, width=300, height=500)
        self.button = {}
        self.closebtn = Button(self.root, text="Back",
                               command=lambda: self.root.destroy())
        self.closebtn.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        self.updateGameScreen()
        self.root.mainloop()

    def updateGameScreen(self):
        self.game_status = board_check(self.board) or self.game_status

        for i, key in enumerate(self.board):
            btn_state = NORMAL if self.board[key] == ' ' else DISABLED
            if (game_mode == "PvC" and not self.is_player_turn()) or self.game_status in ["X_win", "O_win", "draw"]:
                btn_state = DISABLED
            self.button[i] = Button(self.gscreen, text=self.board[key], state=btn_state, command=lambda x=key: self.play(
                x), disabledforeground="black").grid(row=i//3, column=i % 3, sticky="nsew", ipadx=10, ipady=10)
        self.gscreen.pack()

        if self.game_status in ["X_turn", "O_turn"]:
            if game_mode == "PvC":
                if self.is_player_turn():
                    self.turnlabel.configure(
                        text=" Your Turn ", bg="blue", fg="white")
                else:
                    self.turnlabel.configure(
                        text=" Computer's Turn... ", bg="orange", fg="white")
                    self.computer_play()
            elif game_mode == "PvP":
                txt_turn = " X's Turn " if self.game_status == 'X_turn' else " O's Turn "
                color_turn = "blue" if self.game_status == 'X_turn' else "orange"
                self.turnlabel.configure(
                    text=txt_turn, bg=color_turn, fg="white")
        elif self.game_status == "draw":
            self.turnlabel.configure(
                text=" Draw, but we must settle this.. Play again! ", bg="grey", fg="white")
        elif game_mode == "PvC":
            if (self.game_status == "X_win" and p1_symbol == "X") or (self.game_status == "O_win" and p1_symbol == "O"):
                self.turnlabel.configure(text=random.choice(
                    win_messages), bg="green", fg="white")
            else:
                self.turnlabel.configure(text=random.choice(
                    lose_messages), bg="red", fg="white")
        elif game_mode == "PvP":
            if self.game_status == "X_win":
                self.turnlabel.configure(
                    text=" X Won! ", bg="green", fg="white")
            elif self.game_status == "O_win":
                self.turnlabel.configure(
                    text=" O Won! ", bg="green", fg="white")

    def is_player_turn(self):
        if game_mode == 2 or\
                self.game_status == 'X_turn' and p1_symbol == 'X' or\
                self.game_status == 'O_turn' and p1_symbol == 'O':
            return True  # player's turn
        else:
            return False  # computer's turn

    def play(self, pos):

        if self.game_status == "X_turn":
            self.board[pos] = "X"
            self.game_status = "O_turn"
        elif self.game_status == "O_turn":
            self.board[pos] = "O"
            self.game_status = "X_turn"
        print("User played:", pos)
        print("BOARD:", self.board)
        self.updateGameScreen()

    def computer_play(self, wait=1):
        Timer(wait, self.computer_play_).start()

# Linux kill all suspended processes
# ps -ef | grep python | grep -v grep | awk '{print $2}' | xargs kill -9

    def computer_play_(self):
        available_pos = [key for key,
                         value in self.board.items() if value == ' ']
        pos = random.choice(available_pos)
        self.board[pos] = "O" if p1_symbol == "X" else "X"
        if self.game_status == "X_turn":
            self.game_status = "O_turn"
        elif self.game_status == "O_turn":
            self.game_status = "X_turn"
        print("Computer played:", pos)
        print("BOARD:", self.board)
        self.updateGameScreen()


loadMainMenu()
