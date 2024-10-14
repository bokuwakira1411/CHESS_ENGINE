from const_val import *
from square import Square
from piece import *
from move import Move
import copy
from copy import deepcopy
class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.check_king_piece = None
        self.check_king_move = None
        
    def undo_move(self, move):
        initial = move.initial
        final = move.final
        piece = self.squares[final.row][final.col].piece

        # Khôi phục quân cờ về ô ban đầu
        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = None

        # Thiết lập lại trạng thái di chuyển của quân cờ
        piece.moved = False # Hoặc bạn có thể lưu trữ nước đi trước đó nếu cầ
    def calc_moves(self, piece, row, col, bool = True):
        
        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        initial_piece = self.squares[row][col].piece
                        for d_row in range(row + piece.dir, possible_move_row + piece.dir, piece.dir):
                            if self.squares[d_row][col].has_team_piece(initial_piece.color) or self.squares[d_row][col].has_rival_piece(initial_piece.color):
                                break
                        # check potencial checks
                            if bool:
                                    if not self.check_King(piece, move):
                                        # append new move
                                        piece.add_move(move)
                            else:
                                        # append new move
                                        piece.add_move(move)
                    # blocked
                    else: break
                # not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        
                        move = Move(initial, final)
                        if bool:
                            if not self.check_King(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]
            for move in possible_moves:
                move_row, move_col = move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty() or self.squares[move_row][move_col].has_rival_piece(piece.color):
                        
                        initial = Square(row, col)
                        final_piece = self.squares[row][col].piece
                        final = Square(move_row, move_col, final_piece)
                        
                        move = Move(initial, final)
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                            break 
                        elif bool and final_piece != None:
                            if not self.check_King(final_piece, move):
                                piece.add_move(move)
                        else:
                                piece.add_move(move)
                    else:
                        break
                
        def king_moves():
            possible_moves = [
                (row-1, col),
                (row-1, col-1),
                (row-1, col+1),
                (row+1, col),
                (row+1, col-1),
                (row+1, col+1),
                (row, col-1),
                (row, col+1),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                        if self.squares[possible_move_row][possible_move_col].empty_or_rival(piece.color):
                        
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)                            
                            move = Move(initial, final)
                            if bool and final_piece != None:
                                if not self.check_King(final_piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook
                                initial = Square(row,0)
                                final_piece = self.squares[possible_move_row][possible_move_col].piece
                                final = Square(row, 3, final_piece)
                                move_rook = Move(initial, final)
                                left_rook.add_move(move_rook)

                                initial = Square(row, col)
                                final = Square(row, 2)
                                move_king = Move(initial, final)
                                if bool:
                                    if not self.check_King(piece, move_king) and not self.check_King(left_rook, move_rook):
                                        piece.add_move(move_king)
                                        left_rook.add_move(move_rook)
                                else:
                                        piece.add_move(move_king)
                                        left_rook.add_move(move_rook)

                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook
                                initial = Square(row,7)
                                final = Square(row, 5)
                                move_rook = Move(initial, final)
                                
                                initial = Square(row, col)
                                final = Square(row, 6)
                
                                move_king = Move(initial, final)
                                if bool:
                                    if not self.check_King(piece, move_king) and not self.check_King(right_rook, move_rook):
                                        piece.add_move(move_king)
                                        right_rook.add_move(move_rook)
                                else:
                                        piece.add_move(move_king)
                                        right_rook.add_move(move_rook)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row_incr + row
                possible_move_col = col_incr + col
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):                    
                        initial = Square(row, col)
                        final_piece = self.squares[row][col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                        elif self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.check_King(final_piece, move):
                                    piece.add_move(move)
                            else:
                                    piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                                if not self.check_King(final_piece, move):
                                    piece.add_move(move)
                            else:
                                    piece.add_move(move)
                            break
                    else: break
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr



        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1,1), #up_right
                (-1,-1), #up_left
                (1,1) ,# down_right
                (1,-1) # down_left
            ])
        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1,0), #up
                (0,-1), # left
                (1,0), #down
                (0,1), #right
                
            ])
        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1,1), #up_right
                (-1,-1), #up_left
                (1,1), # down_right
                (1,-1), # down_left
                (-1,0), #up
                (0,-1), # left
                (1,0), #down
                (0,1) #right
            ])
        elif isinstance(piece, King):
            king_moves()
    
    def check_King(self, piece, move):
        t_piece = copy.deepcopy(piece)
        t_board = copy.deepcopy(self)
        t_board.move(t_piece, move)
        for r in range(ROWS):
            for c in range(COLS):
                if t_board.squares[r][c].has_rival_piece(t_piece.color):
                    p = t_board.squares[r][c].piece
                    p.moves = p.clear_moves()
                    t_board.calc_moves(p, r, c, bool = False)
                    for m in p.moves:
                        if isinstance(self.squares[m.final.row][m.final.col].piece, King) and self.squares[m.initial.row][m.initial.col].piece.color == 'white':
                            self.check_king_piece = self.squares[m.initial.row][m.initial.col].piece
                            return True
        return False

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, )
    def check_pawn_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        if isinstance(piece, Pawn):
            self.check_pawn_promotion(piece, final)
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                
                if(len(rook.moves) >=1):    
                    self.move(rook, rook.moves[-1])
        piece.moved = True
        piece.moves = piece.clear_moves()
        self.last_move = move
    
    def castling(self, initial, final):
            return abs(initial.col - final.col) == 2
    
    def valid_move(self, piece, move):
        return move in piece.moves
    
    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6,7)    
        else:
            row_pawn, row_other = (1,0) 
        #pawn
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn,col, Pawn(color))
        #knights
        self.squares[4][2] = Square(4, 2, Bishop('white'))
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
    
    def get_possible_moves(self, color):
        possible_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].piece != None and self.squares[row][col].piece.color == color :
                    self.calc_moves(self.squares[row][col].piece, row, col)
                    possible_moves.extend(self.squares[row][col].piece.moves)
        if not possible_moves:
            print('none')
        return possible_moves
    

    def check_King_all_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if not self.squares[row][col].isempty():
                    cur_piece = self.squares[row][col].piece
                    for move in cur_piece.moves:
                        fi_piece = self.squares[move.final.row][move.final.col].piece
                        if  fi_piece is not None and fi_piece.name == 'King' and fi_piece.color != cur_piece.color:
                            print('fi_piece')
                            self.check_king_piece = fi_piece
                            self.check_king_move = move
            print('No piece')
        return False

    def is_stalemate(self):
        if self.check_King_all_board() == True:
            return False
        if self.get_possible_moves('white') == [] or self.get_possible_moves('black') == []:
            return True
        
    def is_endgame(self):
        white_pieces = 0
        black_pieces = 0
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece != None and piece.color == "white":
                    white_pieces += 1
                elif piece !=None and piece.color == "black":
                    black_pieces += 1
        if white_pieces <= 7 or black_pieces <= 7 or (white_pieces + black_pieces <= 14):
            return white_pieces, black_pieces, True
        else:
            return white_pieces, black_pieces, False
    def is_game_over(self):
        white_king_present = False
        black_king_present = False

        for r in range(ROWS):
            for c in range(COLS):
                piece = self.squares[r][c].piece
                if isinstance(piece, King):
                    if piece.color == 'white':
                        white_king_present = True
                    elif piece.color == 'black':
                        black_king_present = True

    # Kiểm tra xem có vua trắng và vua đen trên bàn cờ
        if not white_king_present:
            print("AI wins!")
            return True  # Trò chơi kết thúc nếu không còn vua trắng
        elif not black_king_present:
            print("Player wins!")
            return True  # Trò chơi kết thúc nếu không còn vua đen

        return False  # Trò chơi vẫn tiếp tục