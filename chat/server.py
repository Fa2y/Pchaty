	from chat import *
	import eventlet
	import eventlet.queue as queue

	send_queues = {}


	def handle_client_recv(s,address):
		rest = bytes()
		try:
			(msgs, rest) = recv_msgs(s,address)
		except (ConnectionError, EOFError):
			handle_disconnect(s, addr)
		for msg in msgs:
			msg = '{}: {}'.format(address, msg)
			print(msg)
			broadcast_msg(msg)

	def handle_client_send(s, q,addr):
		while True:
			msg = q.get()
			if msg == None: break
			try:
				send_msg(s, msg)
			except (ConnectionError, BrokenPipe):
				handle_disconnect(s,addr)
				break
	def broadcast_msg(msg):
		for q in send_queues.values():
			q.put(msg)

	def handle_disconnect(s,addr):
		fd = s.fileno()
		q = send_queues.get(fd, None)
		if q:
			q.put(None)
			del send_queues[fd]
			addr = s.getpeername()
			print('Client {} disconnected'.format(addr))
			s.close()


	if __name__ == '__main__':
		server = eventlet.listen((HOST, PORT))
		addr = server.getsockname()
		print('Listening on {}'.format(addr))
		
		while True:
			cs,addr = server.accept()		
			q = queue.Queue()
			send_queues[cs.fileno()] = q
			eventlet.spawn_n(handle_client_recv,cs,addr)
			eventlet.spawn_n(handle_client_send,cs,q,addr)
			print('Connection from {}'.format(addr))
