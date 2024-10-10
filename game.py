import pygame
from const_val import *
from board import Board
from dragger import Dragger
from chessAI import chessAI
class Game:
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()
        self.ai = chessAI(next_player="black")

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col)%2 == 0:
                    color = (234,235,200)
                else:
                    color = (119, 154, 88)
                rectangle  = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rectangle)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col*SQSIZE + SQSIZE//2, row*SQSIZE+SQSIZE//2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = '#e6e600'
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                color = (244,247,116) if (pos.row + pos.col) %2 == 0 else (172, 195,51)
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        if self.next_player == 'black':  # Check if it's AI's turn
            self.AI_move()
    
    def AI_move(self):
        best_move = self.ai.find_best_move(self.board)

        if best_move:
            # Tô màu ô có thể di chuyển
            color = (230, 230, 0)  # Màu cho nước đi của AI
            rect = (best_move.final.col * SQSIZE, best_move.final.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(self.screen, color, rect)  # Tô màu ô nước đi

            # Thực hiện nước đi
            self.board.move(best_move.initial.piece, best_move)
