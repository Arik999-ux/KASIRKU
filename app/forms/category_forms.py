from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.category import Category

class CategoryForm(FlaskForm):
    name = StringField('Nama Kategori', validators=[
        DataRequired(message='Nama kategori wajib diisi.'),
        Length(min=2, max=100, message='Nama kategori minimal 2 karakter.')
    ])
    description = TextAreaField('Deskripsi', validators=[
        Length(max=255, message='Deskripsi maksimal 255 karakter.')
    ])
    submit = SubmitField('Simpan')

    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category:
            raise ValidationError('Nama kategori sudah digunakan.')