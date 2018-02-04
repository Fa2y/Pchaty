import socket

HOST = ''
PORT = 1234

def create_listen_socket(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(100)
	return s

def recv_msg(s):
	data = bytearray()
	msg = ''
	while not msg:
		recvd = s.recv(4096)
		if not recvd:
			raise ConnectionError()
		data = data + recvd
		if b'\0' in recvd:
			msg = data.rstrip(b'\0')
	msg = msg.decode('utf-8')
	return msg

def pre_msg(msg):
	msg += '\0'
	return msg.encode('utf-8')

def send_msg(s,msg):
	data = pre_msg(msg)
	s.sendall(data)

