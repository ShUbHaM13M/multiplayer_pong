import json
import socket

class Network(object):
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = 'localhost' 
		self.port = 5050
		self.addr = (self.host, self.port)
		self.id = self.connect()

	def connect(self):
		self.client.connect(self.addr)
		return self.client.recv(1024).decode()
	
	def send(self, data):
		try:
			self.client.send(str.encode(data))
			recieved = self.client.recv(2048).decode()
			return recieved
		except socket.error as e:
			return str(e)

if __name__ == '__main__':
	network = Network()
	for i in range(4):
		network.send("Hello world")