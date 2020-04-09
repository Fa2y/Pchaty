import npyscreen
import sys, socket, threading
import chat


HOST = "Fa2y"
PORT = chat.PORT
CLIENT = None

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
class mainForm(npyscreen.Form):
	"""main form that contain all the other forms and widgets
	using SplitFrom to separate area """
	def create(self):
		self.server = self.add(msgLog,name = 'Messages : ',max_height=10,rely=1,editable=False)
		self.msg = self.add(npyscreen.TitleText,name = 'ClientName',editable = True)

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
		npyscreen.notify_wait("Connecting...")
		global HOST, PORT,CLIENT
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
			self.parentApp.editw = 0

	def on_cancel(self):
		self.parentApp.setNextForm(None)

if __name__ == '__main__':
	TestApp = App().run()