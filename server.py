from socket import *
import socket
from time import ctime

HOST = input("Enter the hostname: ")
PORT = input("Entrt the port: ")
BUFSIZ = 1024
ADDR = (HOST,int(PORT))

if __name__ == '__main__':
	s = socket.socket(AF_INET,SOCK_STREAM)
	s.bind(ADDR)
	s.listen(5)
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	while True:
		print('Server waiting for connection...')
		cs, addr=s.accept()
		print('Client connected from: ',addr)

		while True:
			data = cs.recv(BUFSIZ)
			if not data or data.decode('utf-8') == 'END':
				break
			print("Received from client: %s" % data.decode('utf-8'))
			print("Sending the server time to client: %s" %ctime())
			try:
				cs.send(bytes(ctime(),'utf-8'))
			except KeyboardInterrupt:
				print("Exited by user")
		cs.close()
	s.close()

