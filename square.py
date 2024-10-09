class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    def has_piece(self):
        return self.piece != None
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def empty_or_rival(self, color):
        return (not self.has_piece()) or self.has_rival_piece(color)
    def isempty(self):
        return self.has_piece() == False
    @staticmethod
    def in_range(*args):        #check co ra ngoai bang hay ko  
        for arg in args:
            if arg<0 or arg>7:
                return False
        return True

