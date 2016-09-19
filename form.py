from wtforms import Form,StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [ DataRequired()])

class SearchForm(Form):
    search = StringField('whois')
    submit = SubmitField('Submit')