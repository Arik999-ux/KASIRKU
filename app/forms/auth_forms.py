from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username wajib diisi.'),
        Length(min=3, max=80, message='Username minimal 3 karakter.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email wajib diisi.'),
        Email(message='Format email tidak valid.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi.'),
        Length(min=6, message='Password minimal 6 karakter.')
    ])
    confirm_password = PasswordField('Konfirmasi Password', validators=[
        DataRequired(message='Konfirmasi password wajib diisi.'),
        EqualTo('password', message='Password tidak cocok.')
    ])
    submit = SubmitField('Daftar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah digunakan.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah digunakan.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username wajib diisi.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password wajib diisi.')
    ])
    submit = SubmitField('Masuk')