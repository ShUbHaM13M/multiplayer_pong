from enum import Enum
import json
import sys
import pygame
from client import Network
from ball import Ball
from player import Player

class Game:
	def __init__(self, width, height):
		self.net = Network()
		print(f'Player id: {self.net.id}')
		self.state = {
			self.net.id: 20,
			"ball": [50, 50],
			"game_started": False
		}
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.display = pygame.Surface((self.width // 2, self.height // 2))
		self.player = Player(10, 20, 10, 40)
		self.player2 = Player(self.width // 2 - 20, 20, 10, 40)
		self.ball = Ball(self.state['ball'][0], self.state['ball'][1], 10, 10, (0, 255, 255))
		self.clock = pygame.time.Clock()
		self.game_started = False

	def start(self):
		is_running = True
		while is_running:
			self.display.fill((0, 0, 0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					is_running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE: self.game_started = True

			keys = pygame.key.get_pressed()
			if keys[pygame.K_DOWN]:
				if self.net.id == 'player1':
					if self.player.rect.y < self.height // 2 - self.player.rect.height:
						self.player.move(Player.move_dir.DOWN)
				elif self.net.id == 'player2':
					if self.player2.rect.y < self.height // 2 - self.player2.rect.height:
						self.player2.move(Player.move_dir.DOWN)

			if keys[pygame.K_UP]:
				if self.net.id == 'player1':
					if self.player.rect.y > 0:
						self.player.move(Player.move_dir.UP)
				elif self.net.id == 'player2':
					if self.player2.rect.y > 0:
						self.player2.move(Player.move_dir.UP)

			data = self.parse_data(self.send_data())

			if self.net.id == 'player1':
				self.player2.rect.y = data['player2']
			elif self.net.id == 'player2':
				self.player.rect.y = data['player1']

			ball_pos = data['ball']			
			self.ball.update_pos(*ball_pos)
			if self.game_started:
				self.ball.move((self.player, self.player2), self.display)
			else:
				self.game_started = data.get("game_started", False)

			self.update()

	def send_data(self):
		self.state = {
			"ball": [self.ball.rect.x, self.ball.rect.y],
			self.net.id: self.player.rect.y if self.net.id == "player1" else self.player2.rect.y,
			"game_started": self.game_started
		}
		reply = self.net.send(json.dumps(self.state))
		return reply

	@staticmethod
	def parse_data(data):
		try:
			return json.loads(data)
		except Exception as e:
			print(e)
			return {"player2": 0, "ball": [50, 50], "player1": 0, "game_started": False}

	def update(self):
		
		for y in range(0, self.height // 2, 30):
			pygame.draw.rect(self.display, (255, 255, 255), (self.display.get_width() // 2 - 2, y, 4, 20))

		self.player.render(self.display)
		self.player2.render(self.display)
		self.ball.render(self.display)
		self.screen.blit(pygame.transform.scale(self.display, (self.width, self.height)), (0, 0))
		pygame.display.update()
		pygame.display.set_caption(f"Pong: {int(self.clock.get_fps())}")
		self.clock.tick(60)



if __name__ == '__main__':
	game = Game(500, 500)
	game.start()