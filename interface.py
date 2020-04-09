import npyscreen, curses
import sys, socket, threading, time
import chat


HOST = "Fa2y"
PORT = chat.PORT
CLIENT = None
REST = bytearray()

class App(npyscreen.NPSAppManaged):
		
	def onStart(self):
		""" we will use to manage our forms"""
		self.addForm('Message', mainForm,name ='Pchaty :')
		self.addForm('MAIN',loginForm,name = 'Login :')
		pass
	def while_waiting(self):
		#here we will put stuff that excute when user input state
		pass
	#there is Form.ativate to indicate if the form is active or not 
	def onCleanExit(self):
		#put here exit task like save and stuff
		pass

#Form.nextrely is when the next widget going to placed and also we nextrelx for axis-x
class mainForm(npyscreen.FormBaseNew):
	"""main form that contain all the other forms and widgets
	using SplitFrom to separate area """
	def create(self):
		global REST
		column_height = terminal_dimensions()[0] - 9
		self.widget_rooms = self.add(
			Column,
			name       = "ROOMS",
			relx       = 2,
			rely       = 2,
			max_width  = 20,
			max_height = 10
		)
		self.widget_channels = self.add(
			Column,
			name       = "CHANNELS",
			relx       = 2,
			rely       = 12,
			max_width  = 20,
			max_height = 12
		)
		self.widget_messages = self.add(
			Column,
			name       = "MESSAGES",
			relx       = 23,
			rely       = 2,
			max_height = column_height

		)
		self.widget_input = self.add(
			InputBox,
			name       = "INPUT",
			max_height = 5,
			max_width  = 121
		)
		self.widget_sendmsg = self.add(
			SendMsg,
			name       = "SEND",
			relx       = terminal_dimensions()[1]-12,
			rely       = terminal_dimensions()[0]-5,
		)
		self.widget_input.resize
		thread = threading.Thread(target=self.Waiting_msgs)
		thread.daemon = True
		thread.start()
		self.widget_input.value = str(terminal_dimensions())

	def Waiting_msgs(self):
		global REST, CLIENT
		while True:
			time.sleep(0.5)
			if CLIENT:				
				try:
					(msgs, REST) = chat.recv_msgs(CLIENT.getsock(), REST)
					for msg in msgs:
						self.widget_messages.values.append(self.parse_msg(msg))
						self.display()
				except ConnectionError:
					npyscreen.notify_wait("Connection Error:Upon message receiving.")
					CLIEN.getsock().close()
				except AttributeError:
					pass

	def parse_msg(self,msg):
		return msg.split(":")[0]+":"+msg.split(":")[2][3:-1]

class Column(npyscreen.BoxTitle):
    def resize(self):
        self.max_height = int(0.73 * terminal_dimensions()[0])

class SendMsg(npyscreen.ButtonPress):
	def whenPressed(self):
		if self.parent.widget_input.value:
			try:
				chat.send_msg(CLIENT.getsock(), self.parent.widget_input.value)  # Blocks until sent
				self.parent.widget_input.value = ""
				self.display()
			except (BrokenPipeError, ConnectionError):
				npyscreen.notify_wait("Connection Error: Message not sent!")


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit




def terminal_dimensions():
    return curses.initscr().getmaxyx()

class msgLog(npyscreen.MultiLineEdit):
	def display_value(self,vl):
		return "Username : %s" %vl


class loginForm(npyscreen.ActionPopup):
	""" the form of login into chat app"""
	# def afterEditing(self):
	# 	#the next form after done with loging form
	# 	self.parentApp.setNextForm("Message")

	def create(self):
		self.show_atx = 33
		self.show_aty = 8

		self.msg = self.add(npyscreen.TitleFixedText, name = "Choose you settings:")
		self.server1 = self.add(npyscreen.TitleText,name = 'Server : ', value = 'Fa2y')
		self.port = self.add(npyscreen.TitleText,name = 'Port : ', value = '4040')
		self.nick = self.add(npyscreen.TitleText,name = 'NickName : ')
	def on_ok(self):
		#Connect
		global HOST, PORT, CLIENT, CLIENT_READY
		HOST = self.server1.value
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((HOST, PORT))
		except:
			npyscreen.notify_wait("Server is down or the setting are wrong, try again...")
			return 1
		client = chat.Client(sock)
		client.setname(self.nick.value)
		try:
			chat.send_msg(sock,client.getname())
			resp = chat.recv_msg(sock)
			if 'Error:duplicate' in resp:
				raise chat.ClientExsit()
			CLIENT = client
			self.parentApp.setNextForm('Message')
		except (BrokenPipeError, ConnectionError):
			sys.stdout.flush()
			npyscreen.notify_wait("Connection Error, Try again!")
		except chat.ClientExsit:
			npyscreen.notify_wait("User with this name already exist")

	def on_cancel(self):
		self.parentApp.setNextForm(None)





if __name__ == '__main__':
	TestApp = App().run()