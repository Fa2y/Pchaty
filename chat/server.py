from chat import *

def handle_client(s,addr):
	try:
		msg = recv_msg(s)
		print('{}: {}'.format(addr,msg))
		send_msg(s,msg)
	except (ConnectionError, BrokenPipeError):
		print("Socket error")
	finally:
		print('Closed connection to {}'.format(addr))
		s.close()

if __name__ == '__main__':
	ls = create_listen_socket(HOST,PORT)
	addr = ls.getsockname()
	print('Listening on {}'.format(addr))
	
	while True:
		cs,addr = ls.accept()
		print('Connection from {}'.format(addr))
		handle_client(cs,addr)


