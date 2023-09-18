import pygame
import random
from .Square import Square
from .Knight import Knight
from .Pawn import Pawn

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.knight = Knight((0,0),self)
        self.pawn_positions = []
        self.squares = self.generate_squares()
        self.setup_board()

    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x, y, self.tile_width, self.tile_height))
        return output

    def get_piece_from_position(self, pos):
        for position in self.pawn_positions:
            if position == pos:
                return True
        return False

    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def setup_board(self):

        self.pawn_positions = random.sample([(x, y) for x in range(8) for y in range(8)], 13)
        print(self.pawn_positions)

        for y in range(8):
            for x in range(8):
                square = self.get_square_from_pos((x, y))

                if (x, y) == self.pawn_positions[0]:
                    square.occupying_piece = self.knight
                    self.knight.pos = (x,y)
                elif (x, y) in self.pawn_positions[1:]:
                    square.occupying_piece = Pawn((x, y), self)

    def draw(self, display,coords):
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True

        for square in self.squares:
            square.draw(display)

        if coords != 0:
            self.knight.pos = coords
            x, y = self.knight.pos
            x, y = x * self.tile_width, y * self.tile_height
            knight = self.knight
            display.blit(knight.img, (x, y))

