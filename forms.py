from flask.ext.wtf import Form, TextField, TextAreaField, validators
from flask.ext.mail import Message
from app import mail
from app import app

class EditPageForm(Form):
	page = TextAreaField('page', validators = [validators.Required()])


class AddPostForm(Form):
	title = TextField('title', validators = [validators.Required()])
	page = TextAreaField('page', validators = [validators.Required()])

class ContactForm(Form):
	subject = TextField('subject', validators = [validators.Required()])
	email = TextField('email', validators = [validators.Email(), validators.Required()])
	message = TextAreaField('message', validators = [validators.Required()])

	def send(self):
		msg = Message(self.subject.data, recipients=['info@southbaycircus.com'], reply_to=self.email.data)
		msg.body = "%s" % self.message.data
		mail.send(msg)