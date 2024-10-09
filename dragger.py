import pygame
from const_val import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
    
    def update_blit(self, surface):
        #self.piece.set_texture(size=128)
        texture = self.piece.texture

        img = pygame.image.load(texture)
        img_center = [self.mouseX, self.mouseY]
        self.piece.texture_rect = img.get_rect(center = img_center)
        surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, position):
        self.mouseX = position[0]
        self.mouseY = position[1]
    
    def initial_rowcol(self, position):
        self.initial_row = position[1] // SQSIZE
        self.initial_col = position[0] // SQSIZE
    
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undrag(self):
        self.piece = None
        self.dragging = False
