from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models.product import Product
from app.models.category import Category
from app.models.transaction import Transaction
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_transactions = Transaction.query.count()

    today = datetime.utcnow().date()
    transactions_today = Transaction.query.filter(
        db.func.date(Transaction.created_at) == today
    ).all()
    revenue_today = sum(t.total_price for t in transactions_today)

    recent_transactions = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).limit(8).all()

    # Data chart 7 hari terakhir
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_transactions = Transaction.query.filter(
            db.func.date(Transaction.created_at) == day
        ).all()
        revenue = sum(t.total_price for t in day_transactions)
        chart_labels.append(day.strftime('%d %b'))
        chart_data.append(revenue)

    # Top produk terlaris
    from sqlalchemy import func
    top_products = db.session.query(
        Product.name,
        func.sum(Transaction.quantity).label('total_qty'),
        func.sum(Transaction.total_price).label('total_revenue')
    ).join(Transaction, Transaction.product_id == Product.id)\
     .group_by(Product.id)\
     .order_by(func.sum(Transaction.quantity).desc())\
     .limit(5).all()

    return render_template('dashboard/index.html',
        total_products=total_products,
        total_categories=total_categories,
        total_transactions=total_transactions,
        revenue_today=revenue_today,
        recent_transactions=recent_transactions,
        chart_labels=chart_labels,
        chart_data=chart_data,
        top_products=top_products
    )