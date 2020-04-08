import select
import chat
from types import SimpleNamespace
from collections import deque

HOST = chat.HOST
PORT = chat.PORT
clients = {}
channels = {}
rooms = {}
def create_client(sock):
	""" Return an object representing a client """
	client = chat.Client(sock)
	recvd = client.sock.recv(4096)
	if recvd:
		client_name = (recvd.decode('utf-8').split('\0'))[0]
		for clt in clients.values():
			if clt.getname() == client_name:
				raise chat.ClientExsit()
		client.setname(client_name)
	return client
	#SimpleNamespace(sock=sock,rest=bytes(),send_queue=deque())

def broadcast_msg(msg):
	""" Add message to all connected clients' queues """
	data = chat.prep_msg(msg)
	for client in clients.values():
		client.send_queue.append(data)
		poll.register(client.sock, select.POLLOUT)

def send_client_msg(msg,name):
	data = chat.prep_msg(msg)
	for client in clients.values():
		if name == client.getname():
			client.send_queue.append(data)
			poll.register(client.sock,select.POLLOUT)

def getclientsnames():
	return [c.getname() for c in clients.values()]

def getroomsnames():
	return [r.getname() for r in rooms.values()]

def getchannelsnames():
	return [ch.getname() for ch in channels.values()]

def printnames(cmd):
	if cmd == 'channels':
		chs = getchannelsnames()
		print("Channels : ")
		for ch in chs:
			print(' '*4+ch)
	elif cmd == 'rooms':
		rms = getroomsnames()
		print("Rooms : ")
		for rm in rms:
			print(' '*4+rm)
	elif cmd == 'clients':
		clis = getclientsnames()
		print("Clients : ")
		for cl in clis:
			print(' '*4+scl)


if __name__ == '__main__':
	listen_sock = chat.create_listen_socket(HOST, PORT)
	poll = select.poll()
	poll.register(listen_sock, select.POLLIN)
	addr = listen_sock.getsockname()
	print('Listening on {}'.format(addr))

	# This is the event loop. Loop indefinitely, processing events
	# on all sockets when they occur
	while True:
		# Iterate over all sockets with events
		for fd, event in poll.poll():
			# Clear-up a closed socket
			if event & (select.POLLHUP |
						select.POLLERR |
						select.POLLNVAL):
				poll.unregister(fd)
				del clients[fd]

			# Accept new connection, add client to clients dict
			elif fd == listen_sock.fileno():
				client_sock,addr = listen_sock.accept()
				client_sock.setblocking(False)
				fd = client_sock.fileno()
				print(fd)
				try:
					clients[fd] = create_client(client_sock)
					resp_msg = chat.prep_msg("Succesful!")
				except chat.ClientExsit :
					print('Client name duplicate!')
					resp_msg = chat.prep_msg("Error:duplicate")
				client_sock.send(resp_msg)
				if b"Succesful" in resp_msg :
					poll.register(fd, select.POLLIN)
					print('Connection from {}'.format(addr))

			# Handle received data on socket
			elif event & select.POLLIN:
				client = clients[fd]
				addr = client.sock.getpeername()
				recvd = client.sock.recv(4096)
				if not recvd:
					# The client state will get cleaned up in the
					# next iteration of the event loop, as close()
					# sets the socket to POLLNVAL
					client.sock.close()
					print('Client {} disconnected'.format(addr))
					continue
				data = client.rest + recvd
				(msgs, client.rest) = \
								chat.parse_recvd_data(data)
				
				#if command sended its will manipulate it 
				if b'/cmd' in msgs[0]:
					cmd = ([msg.decode('utf-8') for msg in msgs])[0].split(' ')
					if cmd[1] == 'create':
						if cmd[2] == 'channel':
							#creating channel
							channels[cmd[3]] = chat.Channel(clients,cmd[3])
							print("channel created")
					elif cmd[1] == 'connect':
						#select member to connect to him
						print([c.getname() for c in clients.values()])
						if cmd[2] in [c.getname() for c in clients.values()]:
							#creating channel just for two client
							rooms[cmd[2]+client.getname()] = chat.Room(cmd[2],client)
							print("room created : "+cmd[2]+client.getname())
					elif cmd[1] == 'list':
						#gonna list clients or channels or rooms
						printnames(cmd[2])
				else:
					for msg in msgs:
						msg = '{} : {}: {}'.format(client.getname(),addr, msg)
						print(msg)
						broadcast_msg(msg)
						# send_client_msg(msg,client.getname())
				print(clients,channels,rooms)

			# Send message to ready client
			elif event & select.POLLOUT:
				client = clients[fd]
				data = client.send_queue.popleft()
				sent = client.sock.send(data)
				if sent < len(data):
					client.sends.appendleft(data[sent:])
				if not client.send_queue:
					poll.modify(client.sock, select.POLLIN)
