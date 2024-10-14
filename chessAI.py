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
    
    def score_board(self, board):
        piece_score = 0

        if self.is_king_in_check(board, 'black'):
            print(True)
            return +CHECKMATE  
        elif self.is_king_in_check(board, 'white'):
            print(False)
            return -CHECKMATE
        else: 
            for r in range(ROWS):
                for c in range(COLS):
                    square = board.squares[r][c]
                    piece = square.piece

                    if piece is not None:
                        if piece.color == 'white':
                            piece_score += self.calculate_piece_score(piece, r, c)
                            print(piece_score)
                            if isinstance(piece, King):
                                self.wk_row, self.wk_col = r, c  # Lưu vị trí vua trắng
                        else:
                            piece_score += self.calculate_defensive_priority_score(board, piece, r, c)
                            print(piece_score)
                            if isinstance(piece, King):
                                self.bk_row, self.bk_col = r, c  # Lưu vị trí vua đen

            # piece_score += self.endgame_adjustments(board)

        return piece_score
    def calculate_defensive_priority_score(self, board, piece, row, col):
        max_threatening_capture_score = 0
        best_capture_score = 0

        for move in board.get_possible_moves('white'):
            target_square = board.squares[move.final.row][move.final.col]
            if target_square.has_rival_piece('white'):
                threatened_piece = target_square.piece
                max_threatening_capture_score = max(max_threatening_capture_score, abs(threatened_piece.value))

        for move in piece.moves:
            target_square = board.squares[move.final.row][move.final.col]
            if target_square.has_rival_piece('black'):
                captured_piece = target_square.piece
                best_capture_score = max(best_capture_score, captured_piece.value)

        if max_threatening_capture_score > best_capture_score:
            return max_threatening_capture_score  # Trả về giá trị âm nếu bị đe dọa nhiều hơn
        
        return self.calculate_piece_score(piece, row, col) - best_capture_score
    def calculate_piece_score(self, piece, row, col):
        
        if isinstance(piece, Pawn):
            return piece.value + (pawn_scores[row][col] if piece.color == 'white' else -pawn_scores[row][col])
        elif isinstance(piece, Rook):
            return piece.value + (rook_scores[row][col] if piece.color == 'white' else -rook_scores[row][col])
        elif isinstance(piece, Bishop):
            return piece.value + (bishop_scores[row][col] if piece.color == 'white' else -bishop_scores[row][col])
        elif isinstance(piece, Queen):
            return piece.value + (queen_scores[row][col] if piece.color == 'white' else -queen_scores[row][col])
        elif isinstance(piece, King):
            return 0  
        return 0  

    def endgame_adjustments(self, board):
        
        score_adjustment = 0
        white_pieces, black_pieces, endgame_phase = board.is_endgame()

        if endgame_phase:
            
            min_dist = min(abs(self.wk_row - 0), abs(self.wk_row - 7), abs(self.wk_col - 0), abs(self.wk_col - 7))
            score_adjustment += min_dist * 0.1  # Thêm khoảng cách tới góc

            if white_pieces <= 7:
                score_adjustment -= 50  # Trừ điểm nếu quân trắng ít

            # Thêm điểm nếu quân đen ít
            if black_pieces <= 7:
                score_adjustment += 50  # Thêm điểm nếu quân đen ít

        return score_adjustment
        
    def find_random_move(self, board):
        possible_moves = board.get_possible_moves('black')
        return random.choice(possible_moves)
    def find_move_minimax_alpha_beta(self, board, depth, alpha, beta, maximizing):
        best_move = None
        if depth == 0 or board.is_stalemate():
            return best_move, self.score_board(board)
        best_move = None
        
        if maximizing:
                
                possible_moves = board.get_possible_moves('white')
                random.shuffle(possible_moves)
                max_eval = -CHECKMATE

                for move in possible_moves:
                    #if not self.threatened_move(board, move):
                        copy_board = copy.deepcopy(board)
                        init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                        copy_board.move(init_piece, move)

                        # Gọi hàm score_board để tính điểm cho trạng thái mới
                        _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)

                        if curr_eval is None:
                            continue  # Bỏ qua nếu không có giá trị đánh giá hợp lệ

                        if curr_eval > max_eval:
                            max_eval = curr_eval
                            best_move = move

                        alpha = max(alpha, curr_eval)
                        if beta <= alpha:
                            break  # Cắt tỉa

        else:
                possible_moves = board.get_possible_moves('black')
                random.shuffle(possible_moves)
                min_eval = CHECKMATE

                for move in possible_moves:
                    #if not self.threatened_move(board, move):
                        copy_board = copy.deepcopy(board)
                        init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                        copy_board.move(init_piece, move)

                        # Gọi hàm score_board để tính điểm cho trạng thái mới
                        _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, True)

                        if curr_eval is None:
                            continue  # Bỏ qua nếu không có giá trị đánh giá hợp lệ

                        if curr_eval < min_eval:
                            min_eval = curr_eval
                            best_move = move

                        beta = min(beta, curr_eval)
                        if beta <= alpha:
                            break  # Cắt tỉa

        return best_move, max_eval if maximizing else min_eval
    
    def handle_move(self, game_state, color):
        if self.is_king_in_check(game_state, color):
            possible_moves = game_state.get_possible_moves('black')
            copy_board = copy.deepcopy(game_state)
            for move in possible_moves:
                cur_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                cur_piece.moves = cur_piece.clear_moves()
                copy_board.calc_moves(cur_piece, move.initial.row, move.initial.col)
                copy_board.move(cur_piece, move)
                if not self.is_king_in_check(copy_board, cur_piece.color):
                    return move
        return None          
    
    def find_best_move(self, board):
        
        self.best_move = self.find_random_move(board)  # Bắt đầu với nước đi ngẫu nhiên
        self.searching = True
            
        search_thread = threading.Thread(target=self.search_moves, args=(board,))
        search_thread.start()
        search_thread.join(timeout=30)
        self.searching = False

        self.searching = False 
        print(f"Best move found: {self.best_move}")  
        if board.is_game_over():
                None # Thông báo nước đi được tìm thấy
        if not self.is_king_in_check(board, 'black'):
            return self.best_move
        else:
            return self.handle_move(board, 'black')
    def search_moves(self, board):
        best_move, _ = self.find_move_minimax_alpha_beta(board, self.depth, -CHECKMATE, CHECKMATE, False)
        if self.searching:  # Kiểm tra xem có còn đang tìm kiếm không
            self.best_move = best_move
 
    # def handle_check(self, board):
    #     attacking_piece_moves = self.get_attacking_piece_moves(board)
    #     blocking_moves = []
    #     print('HANDLE CHECKKKKKKKKKKKKKKKKKKKKKK')
    #     # Kiểm tra xem có nước đi nào cho quân đen có thể bắt quân tấn công không
    #     for move in board.get_possible_moves('black'):
    #         piece = board.squares[move.initial.row][move.initial.col].piece
    #         if piece and self.can_capture(board, move):
    #             blocking_moves.append(move)
    #     for move in attacking_piece_moves:
    #         result = self.can_block_check(board, move)
    #         if result:
    #             blocking_moves.append(result)
      
    #     if not blocking_moves:
    #         if board.check_king_piece.color == 'white':
    #             return "Checkmate"  
    #     return blocking_moves if blocking_moves else []

    # def get_attacking_piece_moves(self, board):
    #     if board.check_king_piece.color == 'white':
    #         print(len(board.check_king_piece.moves))
    #         return board.check_king_piece.moves

    #     return []

    # def can_block_check(self, board, move):
    #     copy_board = copy.deepcopy(board)  # Tạo bản sao của bàn cờ
    #     piece = copy_board.squares[move.initial.row][move.initial.col].piece
    #     copy_board.move(piece, move)

    #     # Kiểm tra xem vua có còn bị chiếu không
    #     if not copy_board.check_King_all_board(): 
    #         return move  
    #     return None 

    # def can_capture(self, board, move):
    #     target_square = board.squares[move.final.row][move.final.col]
    #     return target_square.has_rival_piece('white')
    def evaluate_position(self, board):
        score = self.score_board(board)
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if not square.isempty():
                    piece = square.piece
                    if piece.color == 'black':
                        # Thêm điểm cho các nước đi của quân đen có thể bắt quân trắng
                        for move in board.get_possible_moves('black'):
                            if board.squares[move.final.row][move.final.col].has_rival_piece('black'):
                                score += board.squares[move.final.row][move.final.col].piece.value
        return score
    
    def is_king_in_check(self, board, color):
        """Kiểm tra xem vua có bị tấn công không."""
        king_position = (self.bk_row, self.bk_col) if color == 'black' else (self.wk_row, self.wk_col)
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_rival_piece(color):
                    rival_piece = square.piece
                    board.calc_moves(rival_piece, row, col)
                    if king_position in [(move.final.row, move.final.col) for move in board.get_possible_moves(rival_piece.color)]:
                        return True  # Vua bị tấn công

        return False  # Vua không bị tấn công
