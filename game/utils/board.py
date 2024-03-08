
import pygame
from utils.widgets import Peg
from utils.constants import *
from random import choice

class Board:
    def __init__(self, position, size, info_callback, end_game_callback):
        self.position = position
        self.size = size
        self.info_callback = info_callback
        self.end_game_callback = end_game_callback

        self.cell_size = (self.size[0] / BOARD_SIZE, self.size[1] / BOARD_SIZE)

        self.pegs = [[Peg(self.position, row, col, self.cell_size) for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]

        self.wins = {X: 0, O: 0}

        self.current_player = choice([X, O])
        self.last_winner = None

        self.init(self.current_player)

    def init(self, starting_player):
        self.moving = False

        self.current_player = starting_player

        self.board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        
        self.board[3][3] = O
        self.board[3][4] = X
        self.board[4][3] = X
        self.board[4][4] = O

        self.cnt = {X: 2, O: 2}

    def reset(self):
        self.init(self.last_winner)
        
    def surrender(self):
        self.wins[-self.current_player] += 1
        self.last_winner = -self.current_player

        opponent = PLAYER_NAMES[-self.current_player]
        self.info_callback(f"The game has been reset! \n {opponent} Player won!")

        # self.current_player = -self.current_player

    # def user_skip(self):
    #     if not self.has_valid_move(-self.current_player):
    #         current = PLAYER_NAMES[self.current_player]
    #         opponent = PLAYER_NAMES[-self.current_player]

    #         self.info_callback(f"{opponent} Player doesn't have a valid move! \n {current} Player must play again!")

    #     else:
    #         current = PLAYER_NAMES[self.current_player]
    #         self.current_player = -self.current_player
    #         self.info_callback(f"Time's up, {current} Player lost their turn!")

    def build_board(self, surface):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                    self.pegs[row][col].draw(surface, (row, col), self.board[row][col], self.is_valid if not self.moving else lambda _, __, ___: False, self.current_player)

    def catch_press(self, mouse_pos):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.pegs[row][col].is_pressed(mouse_pos):
                    return (row, col)
                
        return None
    
    def in_the_board(self, x, y):
        return (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE)

    def is_valid(self, row, col, player):
        if not self.in_the_board(row, col) or self.board[row][col] != EMPTY:
            return False
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == dy == 0:
                    continue

                opp, self_found = False, False
                x, y = row + dx, col + dy

                while self.in_the_board(x, y):
                    if self.board[x][y] == EMPTY:
                        break

                    if self.board[x][y] == player:
                        self_found = True
                        break

                    opp = True
                    x, y = x + dx, y + dy

                if self_found and opp:
                    return True
                
        return False
    
    def has_valid_move(self, player):
        if (self.cnt[X] == 0 or self.cnt[O] == 0):
            return False

        if self.cnt[X] + self.cnt[O] == BOARD_SIZE * BOARD_SIZE:
            return False

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.is_valid(i, j, player):
                    return True
                
        return False
    
    def winner(self):
        if not self.has_valid_move(X) and not self.has_valid_move(O):
            return X if self.cnt[X] > self.cnt[O] else O if self.cnt[X] < self.cnt[O] else 0
        
        return INF
    
    def user_move(self, row, col):
        if not self.is_valid(row, col, self.current_player):
            return False
        
        self.move(row, col, self.current_player)

        return True
    
    def verify_winner(self):
        w = self.last_winner = self.winner()

        if w == X or w == O:
            self.wins[w] += 1
            winner = PLAYER_NAMES[w]
            self.info_callback(f"Congratulations, {winner} Player won!")
            self.end_game_callback()

        elif not self.has_valid_move(-self.current_player):
            current = PLAYER_NAMES[self.current_player]
            opponent = PLAYER_NAMES[-self.current_player]
            self.info_callback(f"{opponent} Player doesn't have a valid move! \n {current} Player must play again!")

        else:
            self.current_player = -self.current_player

    def move(self, x, y, player):
        self.moving = True
        dirs = {}
        cdirs = {}

        self.board[x][y] = player
        self.cnt[player] += 1

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                opp, self_found = False, False
                i, j = x + dx, y + dy

                while self.in_the_board(i, j):
                    if self.board[i][j] == EMPTY:
                        break

                    if self.board[i][j] == player:
                        self_found = True
                        break

                    opp = True
                    i, j = i + dx, j + dy

                if self_found and opp:
                    dirs[(dx, dy)] = (i, j)
                    cdirs[(dx, dy)] = (x + dx, y + dy)

        self.dirs = dirs
        self.cdirs = cdirs
        self.curpl = player

    def move_slowly(self):
        player = self.curpl
        dirs_to_pop = []

        for (dir, maxim), (_, cdir) in zip(self.dirs.items(), self.cdirs.items()):
            dx, dy = dir
            i, j = maxim

            I, J = cdir

            if I != i or J != j:
                self.board[I][J] = player
                self.cnt[X] += player
                self.cnt[O] -= player

                self.cdirs[dir] = (I + dx, J + dy)
            else:
                dirs_to_pop.append(dir)

        for popdir in dirs_to_pop:
            self.dirs.pop(popdir)
            self.cdirs.pop(popdir)
            
        if len(self.dirs) == 0:
            self.moving = False
            self.verify_winner()

        pygame.time.delay(50)
