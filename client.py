import sys, socket, threading
import chat, ssl

HOST = 'Fa2y'
PORT = chat.PORT
def start():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	if len(sys.argv)>1 and sys.argv[1] == '-ssl':
		context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		context.load_verify_locations('certs/cert.pem')
		sock = context.wrap_socket(sock,server_hostname="PChaty")
	client = chat.Client(sock)
	while True:
		print("entry your name : ")
		name = input()
		try:
			chat.send_msg(sock,name)
			resp = chat.recv_msg(sock)
			if 'Error:duplicate' in resp:
				raise chat.ClientExsit()
		except (BrokenPipeError, ConnectionError):
			sys.stdout.flush()
		except chat.ClientExsit:
			print("User with this name already exist")
			continue
		print('Connected to {}:{}'.format(HOST, PORT))
		client.setname(name)
		return client

def handle_input(sock):
	""" Prompt user for message and send it to server """
	print("Type messages, enter to send. 'q' to quit")
	while True:
		msg = input()  # Blocks
		if msg == 'q':
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			break
		try:
			chat.send_msg(sock, msg)  # Blocks until sent
		except (BrokenPipeError, ConnectionError):
			sys.stdout.flush()
			break
def parse_msg(msg):
	return msg.split(":")[0]+":"+msg.split(":")[2][3:-1]

if __name__ == '__main__':
	client = start()
	sock = client.getsock()
	# Create thread for handling user input and message sending
	thread = threading.Thread(target=handle_input,args=[sock],daemon=True)
	thread.start()
	rest = bytes()
	addr = sock.getsockname()
	# Loop indefinitely to receive messages from server
	while True:
		try:
			(msgs, rest) = chat.recv_msgs(sock, rest)  # blocks
			for msg in msgs:
				print(parse_msg(msg))
		except ConnectionError:
			print('Connection to server closed')
			sock.close()
			break
