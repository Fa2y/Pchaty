import sys,socket
import chat as ch

HOST = input("Enter host: ")
PORT = ch.PORT

if __name__ == '__main__':
	while True:
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((HOST,PORT))
			print('\n Connected to {}'.format(HOST,PORT))
			print("Type Msg , entry 'q' to quit")
			msg = input()
			if msg == 'q':	break
			ch.send_msg(s, msg)
			print("Send message: {}".format(msg))
			msg = ch.recv_msg(s)
			print('Received : ' +msg)
		except ConnetionError:
			print('Socket Error')
			break
		finally:
			s.close()
			print('Closed connection to server\n')

