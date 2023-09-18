import pygame

class Pawn:
	def __init__(self, pos, board):

		img_path = '../Chess/pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width, board.tile_height - 30))