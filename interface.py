import npyscreen

class formsManager(npyscreen.NPSAppManaged):
	""" we will use to manage our forms"""
	def onStart(self):
		self.addForm('MAIN', mainForm,name ='Login :')
		self.addForm('mainForm',mainForm,name = 'pchaty')
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
class loginForm(npyscreen.ActionForm):
	""" the form of login into chat app"""
	def afterEditing(self):
		#the next form after done with loging form
		self.parentApp.setNextForm(mainForm)
	def create(self):
		self.OK_BUTTON_TEXT = 'Connect'
		self.server = self.add(npyscreen.TitleText,name = 'Server : ')
		self.port = self.add(npyscreen.TitleText,name = 'Port : ')
		self.nike = self.add(npyscreen.TitleText,name = 'NickName : ')
		self.error = self.add(npyscreen.MultiLineEdit,value = "Message :",max_height=5, rely=6,editable=False)
	def on_ok(self):
		#connect fucntion
		self.parentApp.setNextForm(mainForm)
if __name__ == '__main__':
	TestApp = formsManager().run()