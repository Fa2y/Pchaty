import sys,socket
import chat as ch
import threading

HOST = ch.HOST
PORT = ch.PORT
def handle_input(s):
	print("Type messages, enter to send. 'q' to quit")
	while True:
		msg = input()
		if msg == 'q':
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			break
		try:
			ch.send_msg(s,msg)
		except (BrokenPipeError, ConnectionError):
			print("in handle input fun")
			break

if __name__ == '__main__':
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((HOST,PORT))
		print('\n Connected to {}'.format(HOST,PORT))
		thread = threading.Thread(target=handle_input,args=[s],daemon=True)
		thread.start()
		rest = bytes()
		addr = s.getsockname()
		while True:
			try:
				(msgs, rest) = ch.recv_msgs(s,rest)
				for m in msgs:
					print(m)
			except ConnectionError:
				print('Connection to server closed')
				s.close()
				break
	except ConnectionError:
		print('Socket Error')
	finally:
		s.close()
		print('Closed connection to server\n')
