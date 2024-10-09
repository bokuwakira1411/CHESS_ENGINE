from const_val import *
from square import Square
from piece import *
from move import Move
class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
    
    def calc_moves(self, piece, row, col):
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
                        piece.add_move(move)
                    # when you move , and the board has another piece block your next square
                    else: break
                # if it is in outside of your board
                else:break 

            # diagonal squares
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1,col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
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
                        final = Square(move_row, move_col)
                        #create new move
                        move = Move(initial, final)
                        piece.add_move(move)
        def bishop_moves():
            possible_moves = (
                [1,1]
            )
        def rook_moves():
            pass
        def queen_moves():
            pass
        def king_moves():
            pass
        def straight_line_moves(incres):
            pass

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1,1) #up_right
                (-1,-1) #up_left
                (1,1) # down_right
                (1,-1) # down_left
            ])
        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1,0) #up
                (0,-1) # left
                (1,0) #down
                (0,1) #right
                
            ])
        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1,1) #up_right
                (-1,-1) #up_left
                (1,1) # down_right
                (1,-1) # down_left
                (-1,0) #up
                (0,-1) # left
                (1,0) #down
                (0,1) #right
            ])
        elif isinstance(piece, King):
            king_moves()
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, )

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


