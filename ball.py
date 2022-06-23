import pygame
import random

CYAN = (0, 255, 255)


class Ball:
	def __init__(self, x, y, width, height, color ):
		self.rect = pygame.Rect(x, y, width, height)
		self.border = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
		self.color = color

		self.direction = [-1 if random.randint(0, 1) == 0 else 1 for _ in range(2) ]

	def move(self, players, screen: pygame.Surface):
		screen_height = screen.get_height()
		screen_width = screen.get_width()

		if (self.rect.y < 0 or self.rect.y > screen_height - self.rect.height):
			self.direction[1] *= -1
		
		if (self.rect.x < 0 or self.rect.x > screen_width - self.rect.width):
			self.direction[0] *= -1

		for player in players:
			if player.rect.colliderect(self.border):
				self.direction[0] *= -1
				self.direction[1] *= -1

		self.rect.x += 2 * self.direction[0]
		self.rect.y += 2 * self.direction[1]
		self.border.x += 2 * self.direction [0]
		self.border.y += 2 * self.direction [1]

	def update_pos(self, x, y):
		self.rect.x = x
		self.rect.y = y
		self.border.x = x - 2
		self.border.y = y - 2

	def render(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)
		pygame.draw.rect(screen, self.color, self.border, 1)

if __name__ == "__main__":
	ball = Ball(0, 0, 10, 10, (255, 0, 0))