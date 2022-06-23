from enum import Enum

import pygame


class Player:
	
	class move_dir(Enum):
		DOWN = 0
		UP = 1

	def __init__(self, x, y, width, height):
		self.velocity = 2
		self.rect = pygame.Rect(x, y, width, height)

	def render(self, screen):
		pygame.draw.rect(screen, (255, 255, 255), self.rect)

	def move(self, dir):
		match dir:
			case Player.move_dir.DOWN:
				self.rect.y += self.velocity
			case Player.move_dir.UP:
				self.rect.y -= self.velocity