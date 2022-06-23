import json
import socket, sys
from _thread import *

PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = 'localhost'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

current_id = "player1"
state = {
	"player1": 10,
	"ball": [50, 50],
	"player2": 10,
	"game_started": False
}
data = json.dumps(state)

def threaded_client(conn: socket.socket, addr):
	global current_id, state, data
	connected = True
	conn.send(str.encode(current_id))
	current_id = "player2"

	while connected:
		try: 
			msg = conn.recv(2048).decode(FORMAT)

			recv = json.loads(msg)
			state = {**state, **recv}

			data = json.dumps(state)
			print(data)
			conn.sendall(bytes(data, encoding=FORMAT))
		except Exception as e:
			print(e)
			break

	print("Connection closed")
	conn.close()
	current_id = "player1"

def start():
	server.listen(2)
	print(f'[INITIALIZED]: server listening on {SERVER}')
	while True:
		conn, addr = server.accept()
		print(f'[NEW CONNECTION]: {addr} connected.')
		start_new_thread(threaded_client, (conn, addr))

if __name__ == '__main__':
	start()