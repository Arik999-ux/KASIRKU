from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class TransactionForm(FlaskForm):
    product_id = SelectField('Produk', coerce=int, validators=[
        DataRequired(message='Produk wajib dipilih.')
    ])
    quantity = IntegerField('Jumlah', validators=[
        DataRequired(message='Jumlah wajib diisi.'),
        NumberRange(min=1, message='Jumlah minimal 1.')
    ])
    submit = SubmitField('Proses Transaksi')