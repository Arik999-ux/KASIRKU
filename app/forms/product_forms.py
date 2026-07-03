from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional

class ProductForm(FlaskForm):
    name = StringField('Nama Produk', validators=[
        DataRequired(message='Nama produk wajib diisi.'),
        Length(min=2, max=150, message='Nama produk minimal 2 karakter.')
    ])
    price = FloatField('Harga', validators=[
        DataRequired(message='Harga wajib diisi.'),
        NumberRange(min=0, message='Harga tidak boleh negatif.')
    ])
    stock = IntegerField('Stok', validators=[
        DataRequired(message='Stok wajib diisi.'),
        NumberRange(min=0, message='Stok tidak boleh negatif.')
    ])
    category_id = SelectField('Kategori', coerce=int, validators=[
        DataRequired(message='Kategori wajib dipilih.')
    ])
    image = FileField('Foto Produk', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Format gambar harus jpg, jpeg, png, atau webp.')
    ])
    submit = SubmitField('Simpan')