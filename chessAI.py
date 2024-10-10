from const_val import *
from square import Square
from piece import *
from move import Move
import random
import copy
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
STALEMATE = 0
class chessAI:
    def __init__(self, next_player):
        self.next_player = next_player
        self.depth = 3

    def threatened_move(self, game_state, move):
        # với mỗi nước đi, cho chạy thử nước đi đó trước - nếu có bất kì quân cờ nào của đối thủ có thể ăn được thì trả về True
        initial = move.initial
        init_piece = initial.piece
        final = move.final
        game_state.move(init_piece, move)
        for row in range(ROWS):
            for col in range(COLS):
                    if game_state.squares[row][col].has_rival_piece(init_piece.colo):
                        rival_piece = game_state.squares[row][col]
                        rival_moves = game_state.calc_moves(rival_piece, row, col)
                        if any(pos_move.final == final for pos_move in rival_moves):
                                game_state.undo_move(initial.piece, move)  # Undo t
                                return True
        game_state.undo_move(init_piece, move)  # Undo the simulated move
        return False

    def order_moves(self, board):
        # Với mỗi tập nước đi có thể xảy ra, sắp xếp các nước đi lại - để mỗi lần lấy ra được nước đi làm cho bàn cờ có điểm cao nhất
        sorted_moves = []
        possible_moves = board.get_possible_moves()
        copy_board = copy.deepcopy(board)
        for move in possible_moves:
            piece = move.initial.piece
            score = self.score_board(copy_board.move(piece,move))
            sorted_moves.append((move, score))
            copy_board.undo_move(piece, move)
        sorted_moves.sort(key=lambda x: x[1], reverse= True)
        return [move for move, score in sorted_moves]

    def evaluate_position(self, board):
        #Hàm ước lượng khi chọn nước đi nào sẽ là tối ưu
        if board.check_King():
            return CHECKMATE if self.next_player == "white" else -CHECKMATE
        if board.is_stalemate():
            return STALEMATE
        return self.score_board(board)
    
    def threaded_search(self, possible_moves, depth):

        #Cho chạy ngắt theo quy định(ví dụ 30 giây cho nghỉ, 1000 bước tìm kiếm cho dừng)
        pass

    def set_search_depth(self, depth):
        self.depth = depth

    def log_decision_making(self, possible_moves, score):
        #

        pass
    
    def find_move_minimax_alpha_beta(self, board, depth, alpha, beta, maximizing):
        possible_moves = board.get_possible_moves()
        if depth == 0 or board.check_King_all_board() or board.is_stalemate():
            return None, self.evaluate_position(board)

        best_move = None
        if maximizing:
            max_eval = -CHECKMATE
            for move in possible_moves:
                copy_board = copy.deepcopy(board)
                copy_board.move(move.initial.piece, move)
                _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)
                if curr_eval > max_eval:
                    max_eval = curr_eval
                    best_move = move
                alpha = max(alpha, curr_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = CHECKMATE
            for move in possible_moves:
                copy_board = copy.deepcopy(board)
                copy_board.move(move.initial.piece, move)
                _, curr_eval = self.find_move_minimax_alpha_beta(copy_board,depth - 1, alpha, beta, True)
                if curr_eval < min_eval:
                    min_eval = curr_eval
                    best_move = move
                beta = min(beta, curr_eval)
                if beta <= alpha:
                    break
            return best_move, min_eval
        
    def score_board(self, board):
        """Calculate the score of the board state."""
        piece_score = 0
        k_row, k_col = None, None

        for r in range(ROWS):
            for c in range(COLS):
                square = board.squares[r][c]
                if not square.isempty():
                    piece = square.piece
                    if isinstance(piece, Pawn):
                        piece_score += piece.value + (pawn_scores[r][c] if piece.color == 'white' else -pawn_scores[7 - r][c])
                    elif isinstance(piece, Rook):
                        piece_score += piece.value + (rook_scores[r][c] if piece.color == 'white' else -rook_scores[7 - r][c])
                    elif isinstance(piece, Bishop):
                        piece_score += piece.value + (bishop_scores[r][c] if piece.color == 'white' else -bishop_scores[7 - r][c])
                    elif isinstance(piece, Queen):
                        piece_score += piece.value + (queen_scores[r][c] if piece.color == 'white' else -queen_scores[7 - r][c])
                    elif isinstance(piece, King):
                        if piece.color == 'white':
                            k_row, k_col = r, c

        # Endgame adjustments
        white_pieces, black_pieces, endgame_phase = board.is_endgame()
        if endgame_phase:
            min_dist = min(abs(k_row - 0), abs(k_row - 7), abs(k_col - 0), abs(k_col - 7))
            piece_score += min_dist * 0.1
            if white_pieces <= 7:
                piece_score -= 50
            if black_pieces <= 7:
                piece_score += 50

        return piece_score

    
    def find_best_move(self, board):
        """Find the best move using the minimax algorithm with alpha-beta pruning."""
        best_move, _ = self.find_move_minimax_alpha_beta(board, self.depth, -CHECKMATE, CHECKMATE, True)
        return best_move
    