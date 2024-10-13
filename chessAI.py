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
                if copy_board.squares[move.final.row][move.final.col].has_rival_piece('black'):
                    
                    score = score - 20*board.squares[move.final.row][move.final.col].piece.value
                    

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
                if not square.piece == None:
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
                            self.wk_row, self.wk_col = r, c
                    # If capturing an opponent's piece
                        else:
                            self.bk_row, self.bk_col = r,c
                    if square.has_rival_piece(piece.color):
                        captured_piece = square.piece
                        if captured_piece.color != piece.color:
                            piece_score -= captured_piece.value 
        # Endgame adjustments
        white_pieces, black_pieces, endgame_phase = board.is_endgame()
        if endgame_phase:
            min_dist = min(abs(self.wk_row - 0), abs(self.wk_row - 7), abs(self.wk_col - 0), abs(self.wk_col - 7))
            piece_score += min_dist * 0.1
            if white_pieces <= 7:
                piece_score -= 50
            if black_pieces <= 7:
                piece_score += 50

        return piece_score

    def find_random_move(self, board):
        possible_moves = board.get_possible_moves('black')
        return random.choice(possible_moves)
   
    def find_best_move(self, board):
        # Tìm nước đi ngẫu nhiên trước
        best_move = self.find_random_move(board)

        best_move, score = self.find_move_minimax_alpha_beta(board, 1, -CHECKMATE, CHECKMATE, False)
       
        print(f"Best move found: {best_move}")  # Thông báo nước đi được tìm thấy
        
        return best_move
    def find_move_minimax_alpha_beta(self, board, depth, alpha, beta, maximizing):
        board_hash = self.get_board_hash(board)

        if board_hash in self.visited_states:
            return self.visited_states[board_hash]

        best_move = None

        # Nếu độ sâu là 0 hoặc trạng thái kết thúc
        if depth == 0 or board.is_stalemate():
            return best_move, self.evaluate_position(board)

        if board.check_King_all_board():
            if board.check_king_piece.color == 'white':
                pos_moves = self.handle_check(board)
                curr_eval = None
                for move in pos_moves:
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)

                    if maximizing:
                        if curr_eval > alpha:
                            alpha = curr_eval
                            best_move = move
                    else:
                        if curr_eval < beta:
                            beta = curr_eval
                            best_move = move

                    if beta <= alpha:
                        break  # Cắt tỉa

                self.visited_states[board_hash] = (best_move, curr_eval)
                return best_move, curr_eval

        if maximizing:
            max_eval = -CHECKMATE
            for move in self.order_moves(board):
                # if not self.threatened_move(board, move):
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, False)

                    if curr_eval > max_eval:
                        max_eval = curr_eval
                        best_move = move

                    alpha = max(alpha, curr_eval)
                    if beta <= alpha:
                        break

            self.visited_states[board_hash] = (best_move, max_eval)
            return best_move, max_eval
        else:
            min_eval = CHECKMATE
            for move in self.order_moves(board):
                # if not self.threatened_move(board, move):
                    copy_board = copy.deepcopy(board)
                    init_piece = copy_board.squares[move.initial.row][move.initial.col].piece
                    copy_board.move(init_piece, move)
                    _, curr_eval = self.find_move_minimax_alpha_beta(copy_board, depth - 1, alpha, beta, True)

                    if curr_eval < min_eval:
                        min_eval = curr_eval
                        best_move = move

                    beta = min(beta, curr_eval)
                    if beta <= alpha:
                        break

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
                if copy_board.squares[row][col].has_rival_piece('white'):
                    rival_piece = game_state.squares[row][col].piece
                    game_state.calc_moves(rival_piece, row, col)
                    rival_moves = game_state.get_possible_moves('black')
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
        time.sleep(10) 
        print(f"Best move found: {self.best_move}")  # Thông báo nước đi được tìm thấy
        return self.best_move

    def search_moves(self, board):
        best_move, _ = self.find_move_minimax_alpha_beta(board, self.depth, -CHECKMATE, CHECKMATE, False)
        if self.searching:  # Kiểm tra xem có còn đang tìm kiếm không
            self.best_move = best_move
 
    def handle_check(self, board):
        attacking_piece_moves = self.get_attacking_piece_moves(board)
        blocking_moves = []
        for move in attacking_piece_moves:
            result = self.can_block_check(board, move)
            if result:
                blocking_moves.append(result)

        return blocking_moves if blocking_moves else []
    
    def get_attacking_piece_moves(self, board):
        attacking_moves = []
        
        for row in range(ROWS):
            for col in range(COLS):
                if not board.squares[row][col].isempty():
                    piece = board.squares[row][col].piece
                    # Chỉ xem xét quân cờ trắng
                    if piece.color == 'white':
                        possible_moves = board.get_possible_moves('white')
                        for move in possible_moves:
                            if move.final.row == self.k_row and move.final.col == self.k_col:
                                attacking_moves.append(move)

        return attacking_moves 
    
    def can_block_check(self, board, move):
        copy_board = copy.deepcopy(board)  # Tạo bản sao của bàn cờ
        piece = copy_board.squares[move.initial.row][move.initial.col].piece
        copy_board.move(piece, move)

        if not copy_board.check_king('black'): 
            return move  
        return None 
    
    def can_capture(self, board, move):
        target_square = board.squares[move.final.row][move.final.col]
        if target_square.has_rival_piece('white'):
                return True
        return False
    def evaluate_position(self, board):
        score = self.score_board(board)
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if not square.isempty():
                    piece = square.piece
                    if piece.color == 'white':
                        score += piece.value

                        # Thêm điểm cho các nước đi có thể bắt quân cờ của đối thủ
                        for move in board.get_possible_moves('white'):
                            if self.can_capture(board, move):
                                if not self.threatened_move(board, move):  
                                    score += 10  # Tăng điểm cho nước đi tấn công
                                else:
                                    score -= 5  # Giảm điểm nếu nước đi tấn công bị phản công
                    else:
                        score -= piece.value

                        # Thêm điểm cho các nước đi của quân đen có thể bắt quân trắng
                        for move in board.get_possible_moves('black'):
                            if self.can_capture(board, move):
                                if not self.threatened_move(board, move):
                                    score -= 10  # Giảm điểm cho quân trắng bị tấn công
                                else:
                                    score += 5  # Tăng điểm nếu quân trắng bị tấn công
        return score
    