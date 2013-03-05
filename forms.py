from flask.ext.wtf import Form, TextField, TextAreaField, RadioField, FormField, BooleanField, SelectMultipleField, widgets, validators
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

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

performance_styles = [
						('Aerial Silks', 'Aerial Silks/Static Trapeze'),
						('Acro', 'Acrobats'),
						('Fire Spinning', 'Fire Spinning'),
						('Juggling', 'Juggling'),
						('Partner Juggling', 'Partner Juggling'),
						('Hooping', 'Circus Hooping'),
						('Poi', 'Poi Spinning'),
						('Props', 'Other Props (Walking Ball, Diablos, Rolo Bolos, Bo Staff, etc)'),
						('Clowns', 'Clowns'),
						('Whips', 'Whip Cracking'),
						('Other', 'Other')
					]

booking_message_format = """
Name: %s
Email: %s
Phone Number: %s
				
Performance Time: %s
Performance Location: %s
Budget: %s

Performance Type: %s
Styles Requested: %s
Other Styles: %s

Additional Comments:
%s
"""

class BookingForm(Form):
	name = TextField('Name', validators = [validators.Required()])
	email = TextField('Email', validators = [validators.Email(), validators.Required()])
	phone = TextField('Contact Phone Number', id='phone')

	budget = TextField('Budget')
	time = TextField('Performance Date')
	location = TextAreaField('Performance Location')
	performance_type = RadioField('Performance Type', choices=[('Stage', 'Stage Show'), ('Walkaround', 'Walkaround'), ('Unsure', 'Unsure')])
	performance_styles = MultiCheckboxField('Performance Styles', choices=performance_styles)
	other_style = TextField('If Other, please specify:', id='other_style')
	other = TextAreaField('other')

	def send(self):
		print 'Sending message'
		msg = Message('A Booking Request From %s' % self.name.data, recipients=['booking@southbaycircus.com'], reply_to=self.email.data)
		msg.body = booking_message_format % (self.name.data, self.email.data, self.phone.data, self.time.data, self.location.data, \
				   		self.budget.data, self.performance_type.data, ', '.join(self.performance_styles.data), self.other_style.data, self.other.data)
		mail.send(msg)

