from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.transaction import Transaction
from app.models.product import Product

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # Logika dasar pembuatan transaksi
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        
        product = Product.query.get_or_404(product_id)
        
        if product.stock >= quantity:
            total = product.price * quantity
            
            new_transaction = Transaction(
                user_id=current_user.id,
                product_id=product.id,
                quantity=quantity,
                total_price=total
            )
            
            product.stock -= quantity
            db.session.add(new_transaction)
            db.session.commit()
            
            flash('Transaksi berhasil!', 'success')
        else:
            flash('Stok tidak mencukupi.', 'danger')
            
        return redirect(url_for('transaction.index'))
    
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    products = Product.query.all()
    return render_template('transaction.html', transactions=transactions, products=products)