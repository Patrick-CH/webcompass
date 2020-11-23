from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email


class SigninForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    submit = SubmitField('Register')


class SearchForm(FlaskForm):
    SearchEngine = SelectField("SearchEngine", validators=[DataRequired()], choices=[(0, "Baidu"), (1, "Google"), (2, "Bing")])
    content = StringField("Content", validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField("Search")