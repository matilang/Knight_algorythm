import pygame

class Knight:
	def __init__(self, pos, board):

		img_path = '../Chess/knight.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width, board.tile_height))
		self.pos = pos
		self.board = board
