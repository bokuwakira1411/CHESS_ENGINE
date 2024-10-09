from const_val import *
from square import Square
from piece import *
from move import Move
import random

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
CHECKMATE = 1000
#salemate
class chessAI:
    def __init__(self, board, next_player):
        self.board = board
        self.next_player = next_player
        self.depth = None
    def threatened_move(self, move):
        # với mỗi nước đi, cho chạy thử nước đi đó trước - nếu có bất kì quân cờ nào của đối thủ có thể ăn được thì trả về True
        game_state = self.board
        initial = move.initial
        init_piece = initial.piece
        final = move.final
        game_state.move(init_piece, move)
        for row in range(ROWS):
            for col in range(COLS):
                    if game_state.squares[row][col].has_rival_piece(init_piece.colo):
                        rival_piece = game_state.squares[row][col]
                        rival_moves = game_state.calc_moves(rival_piece, row, col)
                        for pos_move in rival_moves:
                            if pos_move.final == final:
                                return True
        

    def order_moves(self, possible_moves):
        # Với mỗi tập nước đi có thể xảy ra, sắp xếp các nước đi lại - để mỗi lần lấy ra được nước đi làm cho bàn cờ có điểm cao nhất
        sorted_moves = []
        game_state = self.board
        for move in possible_moves:

            self.score_board()
        pass
    def evaluate_position(self):
        #Hàm ước lượng khi chọn nước đi nào sẽ là tối ưu
        pass
    
    def threaded_search(self, possible_moves, depth):
        #Cho chạy ngắt theo quy định(ví dụ 30 giây cho nghỉ, 1000 bước tìm kiếm cho dừng)
        pass

    def set_search_depth(self, depth):
        self.depth = depth

    def log_decision_making(self, possible_moves, score):
        #
        pass
    
    def find_move_minimax_alpha_beta(self, possible_moves, depth, alpha, beta, turn_multiplier):
        global next_move
        if depth == 0:
            return turn_multiplier * self.score_board()
        max_score = -CHECKMATE
        for move in possible_moves:
            pass
            
    def score_board(self):
        game_state = self.board
        if game_state.check_King():
            if self.next_player == "white":
                return CHECKMATE
            else:
                return -CHECKMATE
        # if game_state is stalemate ???
        piece_score = 0
        for r in range(ROWS):
            for c in range(COLS):
                piece = game_state.squares[r][c].piece
                if game_state.isinstance(piece, Pawn):
                    if piece.color == 'white':
                        piece_score += piece.value + pawn_scores[r][c]
                    else:
                        piece_score -= piece.value + pawn_scores[::-1][r][c]

                if game_state.isinstance(piece, Rook):
                    if piece.color == 'white':
                        piece_score += piece.value + rook_scores[r][c]
                    else:
                        piece_score -= piece.value + rook_scores[::-1][r][c]

                if game_state.isinstance(piece, Bishop):
                    if piece.color == 'white':
                        piece_score += piece.value + bishop_scores[r][c]
                    else:
                        piece_score -= piece.value + bishop_scores[::-1][r][c]

                if game_state.isinstance(piece, Queen):
                    if piece.color == 'white':
                        piece_score += piece.value + queen_scores[r][c]
                    else:
                        piece_score -= piece.value + queen_scores[::-1][r][c]

                # if game_state.isinstance(piece, King):
                #     if piece.color == 'white':
                #         piece_score += piece.value + pawn_scores[r][c]
                #     else:
                #         piece_score -= piece.value + pawn_scores[r][c]

        return piece_score
    def find_best_move(self, possible_moves, queue):
        global next_move
        next_move = None
        random.suffle(possible_moves)
        self.find_move_minimax_alpha_beta()
        pass 
