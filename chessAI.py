from const_val import *
from square import Square
from piece import *
from move import Move
import random
import time
import copy
import threading
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
        self.best_move = None
        self.searching = True
        self.visited_states = {}
        self.evaluated_positions = {} 
        self.wk_row = None
        self.wk_col = None
        self.bk_row = None
        self.bk_col = None
    def get_board_hash(self, board):
        return hash(str(board))

    def order_moves(self, board):
        
        sorted_moves = []
        possible_moves = board.get_possible_moves('black')
        print(len(possible_moves))
        copy_board = copy.deepcopy(board)
        for move in possible_moves:
            piece = copy_board.squares[move.initial.row][move.initial.col].piece
            if piece != None:
                copy_board.move(piece, move)
                print(copy_board.squares[move.final.row][move.final.col].piece.name)
                score = self.score_board(copy_board)
                print(score)
                if copy_board.squares[move.final.row][move.final.col].has_rival_piece('black'):
                    score = score - 2*board.squares[move.final.row][move.final.col].piece.value
                sorted_moves.append((move, score))
                copy_board.undo_move(move)
                print(copy_board.squares[move.initial.row][move.initial.col].piece.name)
        sorted_moves.sort(key=lambda x: x[1])
        for move, score in sorted_moves:
            print(score)
        return [move for move, score in sorted_moves]

    def set_search_depth(self, depth):
        self.depth = depth

    # def log_decision_making(self, possible_moves, score):
    #     #

    #     pass
    
    def score_board(self, board):
        """Calculate the score of the board state."""
        piece_score = 0

        for r in range(ROWS):
            for c in range(COLS):
                square = board.squares[r][c]
                if square.piece is not None:  # Sử dụng is not None
                    piece = square.piece

                    if piece.color == 'white':
                        # Tính điểm cho quân trắng
                        if isinstance(piece, Pawn):
                            piece_score += piece.value + pawn_scores[r][c]
                        elif isinstance(piece, Rook):
                            piece_score += piece.value + rook_scores[r][c]
                        elif isinstance(piece, Bishop):
                            piece_score += piece.value + bishop_scores[r][c]
                        elif isinstance(piece, Queen):
                            piece_score += piece.value + queen_scores[r][c]
                        elif isinstance(piece, King):
                            piece_score += piece.value
                            self.wk_row, self.wk_col = r, c  # Lưu vị trí vua trắng

                    else:
                        # Tính điểm cho quân đen (trừ điểm, nên nó sẽ âm)
                        if isinstance(piece, Pawn):
                            piece_score += piece.value - pawn_scores[7 - r][c]
                        elif isinstance(piece, Rook):
                            piece_score += piece.value - rook_scores[7 - r][c]
                        elif isinstance(piece, Bishop):
                            piece_score += piece.value - bishop_scores[7 - r][c]
                        elif isinstance(piece, Queen):
                            piece_score += piece.value - queen_scores[7 - r][c]
                        elif isinstance(piece, King):
                            piece_score += piece.value 
                            self.bk_row, self.bk_col = r, c  # Lưu vị trí vua đen

                    # Trừ điểm cho quân cờ đen nếu có thể bắt quân trắng
                    if square.has_rival_piece('black'):
                        captured_piece = square.piece
                        if captured_piece.color != 'white':
                            piece_score += captured_piece.value  # Trừ điểm cho quân bị bắt
        print(piece_score)
        # Điều chỉnh cho giai đoạn kết thúc
        white_pieces, black_pieces, endgame_phase = board.is_endgame()
        if endgame_phase:
            min_dist = min(abs(self.wk_row - 0), abs(self.wk_row - 7), abs(self.wk_col - 0), abs(self.wk_col - 7))
            piece_score += min_dist * 0.1  # Thêm khoảng cách tới góc
            if white_pieces <= 7:
                piece_score -= 50  # Trừ điểm nếu quân trắng ít
            if black_pieces <= 7:
                piece_score += 50  # Thêm điểm nếu quân đen ít

        return piece_score

    def find_random_move(self, board):
        possible_moves = board.get_possible_moves('black')
        return random.choice(possible_moves)
   
    def find_move_minimax_alpha_beta(self, board, depth, alpha, beta, maximizing):
        board_hash = self.get_board_hash(board)

        if board_hash in self.visited_states:
            return self.visited_states[board_hash]

        # Nếu độ sâu là 0 hoặc trạng thái kết thúc
        if depth == 0 or board.is_stalemate() :
            return None, self.score_board(board)

        best_move = None

        if board.check_King_all_board():
                curr_eval = 0
                pos_moves = self.handle_check(board)
                print(len(pos_moves))
                for move in pos_moves:
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)
                    curr_eval -=10
                    if curr_eval is None:
                        continue  # Bỏ qua nếu không có giá trị đánh giá hợp lệ

                    if curr_eval > alpha:
                        alpha = curr_eval
                        best_move = move

                    if beta <= alpha:
                        break  # Cắt tỉa

                self.visited_states[board_hash] = (best_move, curr_eval)
                return best_move, curr_eval

        # Nếu không ở trong tình huống chiếu
        if maximizing:
            max_eval = -CHECKMATE
            for move in self.order_moves(board):
                if not self.threatened_move(board, move):
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)

                    if curr_eval is None:
                        continue  # Bỏ qua nếu không có giá trị đánh giá hợp lệ

                    if curr_eval > max_eval:
                        max_eval = curr_eval
                        best_move = move

                    alpha = max(alpha, curr_eval)
                    if beta <= alpha:
                        break  # Cắt tỉa

                self.visited_states[board_hash] = (best_move, max_eval)
                return best_move, max_eval
        else:
            min_eval = CHECKMATE
            for move in self.order_moves(board):
                if not self.threatened_move(board, move):
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, True)

                    if curr_eval is None:
                        continue  # Bỏ qua nếu không có giá trị đánh giá hợp lệ

                    if curr_eval < min_eval:
                        min_eval = curr_eval
                        best_move = move

                    beta = min(beta, curr_eval)
                    if beta <= alpha:
                        break  # Cắt tỉa

            self.visited_states[board_hash] = (best_move, min_eval)
            return best_move, min_eval

    def threatened_move(self, game_state, move):
        initial = move.initial
        copy_board = copy.deepcopy(game_state)
        init_piece = copy_board.squares[initial.row][initial.col].piece
        final = move.final
        copy_board.move(init_piece, move)

        # Kiểm tra xem quân vua có bị tấn công không
        for row in range(ROWS):
            for col in range(COLS):
                if copy_board.squares[row][col].has_rival_piece('black'):
                    rival_piece = game_state.squares[row][col].piece
                    game_state.calc_moves(rival_piece, row, col)
                    rival_moves = game_state.get_possible_moves('white')
                    if any(pos_move.final == final for pos_move in rival_moves):  
                        return True

        return False
    def find_best_move(self, board):
        self.best_move = self.find_random_move(board)  # Bắt đầu với nước đi ngẫu nhiên
        self.searching = True
        
        search_thread = threading.Thread(target=self.search_moves, args=(board,))
        search_thread.start()
        search_thread.join(timeout=30)
        self.searching = False
        time.sleep(20) 
        print(f"Best move found: {self.best_move}")  
        if board.is_game_over():
            None # Thông báo nước đi được tìm thấy
        return self.best_move

    def search_moves(self, board):
        best_move, _ = self.find_move_minimax_alpha_beta(board, self.depth, -CHECKMATE, CHECKMATE, False)
        if self.searching:  # Kiểm tra xem có còn đang tìm kiếm không
            self.best_move = best_move
 
    def handle_check(self, board):
        attacking_piece_moves = self.get_attacking_piece_moves(board)
        blocking_moves = []
        print('HANDLE CHECKKKKKKKKKKKKKKKKKKKKKK')
        # Kiểm tra xem có nước đi nào cho quân đen có thể bắt quân tấn công không
        for move in board.get_possible_moves('black'):
            piece = board.squares[move.initial.row][move.initial.col].piece
            if piece and self.can_capture(board, move):
                blocking_moves.append(move)
        for move in attacking_piece_moves:
            result = self.can_block_check(board, move)
            if result:
                blocking_moves.append(result)
      
        if not blocking_moves:
            if board.check_king_piece.color == 'white':
                return "Checkmate"  
        return blocking_moves if blocking_moves else []

    def get_attacking_piece_moves(self, board):
        if board.check_king_piece.color == 'white':
            print(len(board.check_king_piece.moves))
            return board.check_king_piece.moves

        return []

    def can_block_check(self, board, move):
        copy_board = copy.deepcopy(board)  # Tạo bản sao của bàn cờ
        piece = copy_board.squares[move.initial.row][move.initial.col].piece
        copy_board.move(piece, move)

        # Kiểm tra xem vua có còn bị chiếu không
        if not copy_board.check_King_all_board(): 
            return move  
        return None 

    def can_capture(self, board, move):
        target_square = board.squares[move.final.row][move.final.col]
        return target_square.has_rival_piece('white')
    def evaluate_position(self, board):
        score = self.score_board(board)
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if not square.isempty():
                    piece = square.piece
                    if piece.color == 'white':
                        # Thêm điểm cho các nước đi có thể bắt quân cờ của đối thủ
                        for move in board.get_possible_moves('white'):
                            if board.squares[move.final.row][move.final.col].has_rival_piece('white'):
                                score += board.squares[move.final.row][move.final.col].piece.value
                    else:

                        # Thêm điểm cho các nước đi của quân đen có thể bắt quân trắng
                        for move in board.get_possible_moves('black'):
                            if board.squares[move.final.row][move.final.col].has_rival_piece('black'):
                                score += board.squares[move.final.row][move.final.col].piece.value
        return score
    