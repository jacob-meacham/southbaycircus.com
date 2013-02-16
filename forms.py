from flask.ext.wtf import Form, TextField, TextAreaField, validators

class EditPageForm(Form):
	page = TextAreaField('page', validators = [validators.Required()])


class AddPostForm(Form):
	title = TextField('title', validators = [validators.Required()])
	page = TextAreaField('page', validators = [validators.Required()])