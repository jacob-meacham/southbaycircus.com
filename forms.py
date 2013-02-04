from flask.ext.wtf import Form, TextAreaField, validators

class EditPageForm(Form):
	page = TextAreaField('page', validators = [validators.Required()])