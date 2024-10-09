import os
class Piece:
    def __init__(self, name, color, value, texture=None, teture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1   #duong neu trang, am neu den
        self.value = value*value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = teture_rect
    
    def set_texture(self,size=80):
        self.texture = os.path.join(
            f'images/imgs-{size}px/{self.color}_{self.name}.png')
    def clear_moves(self):
        return []
    def add_move(self, move):
        self.moves.append(move)

class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        super().__init__('pawn', color, 1.0)

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 1000.0)
