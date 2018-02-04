from socket import *
import socket
import sys
BUFSIZ = 256
if __name__ == '__main__':
	try:
		s = socket.socket(family=AF_INET,type=SOCK_STREAM,proto=0)
	except socket.error as err:
		print("failed to create a socket")
		print("reason : %s" %str(err))
		sys.exit()
	print("Socket created")

	target_host = input("Enter the target host name to connect: ")
	target_port = input("Enter the target port: ")

	try:
		s.connect((target_host,int(target_port)))
		print("socket connected to %s on port: %s" %(target_host,target_port))
		payload = 'HEY'
		try:
			while True:
				s.send(payload.encode('utf-8'))
				data = s.recv(BUFSIZ)
				print(data)
				more = input("Want to reply  [y/n]:")
				if more.lower() == 'y':
					payload = input("Enter : ")
				else:
					break
		except KeyboardInterrupt:
			print('Exited by user')
	except socket.error as err:
		print("Failed to connect to %s on port %s" %(target_host,target_port))
		print("Reason: %s" %str(err))
		sys.exit()
	s.close()
	

