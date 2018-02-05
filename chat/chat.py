import socket

HOST = '52.17.32.45'
PORT = 1234

def create_listen_socket(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(100)
	return s

def parse_recvd_data(data):
	parts = data.split(b'\0')
	msgs = parts[:-1]
	rest = parts[-1]
	return (msgs, rest)

def recv_msgs(s,data=bytes()):
	msgs = []
	while not msgs:
		recvd = s.recv(4096)
		print(recvd)
		if not recvd:
			raise ConnectionError()
		data = data + (recvd if isinstance(recvd,tuple) else (recvd,))
		(msgs, rest) = parse_recvd_data(data[0].encode())
	msgs = [msg.decode('utf-8') for msg in msgs]
	return (msgs, rest)	

def pre_msg(msg):
	msg += '\0'
	return msg.encode('utf-8')

def send_msg(s,msg):
	data = pre_msg(msg)
	s.sendall(data)
