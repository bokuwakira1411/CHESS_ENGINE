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
    
    def undo_move(self, board, move):
        initial = move.initial
        final = move.final
        init_piece = initial.piece
        board.move(init_piece, final)

    def calc_moves(self, piece, row, col, bool = True):
        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2
            start = row + piece.dir
            end = row + piece.dir*(1 + steps)
            # when you need to move from a start quare to an end square, then the loop in_range are not in the right position immediately.
            # therefore we have its own moving method
            # When pawns go straight, we just need to check the next square if it is empty or not 
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        
                        initial = Square(row, col)
                        
                        final =  Square(possible_move_row, col)
                        move =  Move(initial, final)
                        initial_piece = self.squares[row][col].piece
                        if bool:
                            if not self.check_King(initial_piece, move):
                                piece.add_move(move)                    
                        else:
                                piece.add_move(move)  
                    else: break
        
                else:break 

            # diagonal squares
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1,col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.check_King(final_piece, move):
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
                    if self.squares[move_row][move_col].empty_or_rival(piece.color):
                        #create square cho new move
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        #create new move
                        move = Move(initial, final)
                        if bool and final_piece != None:
                            if not self.check_King(final_piece, move):
                                piece.add_move(move)
                        else:
                                piece.add_move(move)
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                                if not self.check_King(final_piece, move):
                                    piece.add_move(move)
                            else:
                                    piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
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
                if(t_board.squares[r][c].has_rival_piece(t_piece.color)):
                    p = t_board.squares[r][c].piece
                    t_board.calc_moves(p, r, c, bool = False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
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
                if self.squares[row][col].piece != None and self.squares[row][col].piece.color == 'black' :
                    self.calc_moves(self.squares[row][col].piece, row, col)
                    possible_moves.extend(self.squares[row][col].piece.moves)
        if not possible_moves:
            print('none')
        return possible_moves
    
    def check_King_all_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if  not self.squares[row][col].isempty():
                    cur_piece = self.squares[row][col].piece
                    for move in cur_piece.moves:
                        if self.check_King(cur_piece, move):
                            return True
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
                if piece.color == "white":
                    white_pieces += 1
                elif piece.color == "black":
                    black_pieces += 1
        if white_pieces <= 7 or black_pieces <= 7 or (white_pieces + black_pieces <= 14):
            return white_pieces, black_pieces, True
        else:
            return white_pieces, black_pieces, False
    
    