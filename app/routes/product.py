from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.product import Product
from app.models.category import Category
from app.forms.product_forms import ProductForm
import os
import uuid
from werkzeug.utils import secure_filename

product_bp = Blueprint('product', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def save_image(file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename

@product_bp.route('/products')
@login_required
def index():
    products = Product.query.join(Category).order_by(Product.created_at.desc()).all()
    return render_template('product/index.html', products=products)

@product_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        existing = Product.query.filter_by(name=form.name.data).first()
        if existing:
            flash('Nama produk sudah digunakan.', 'danger')
            return render_template('product/create.html', form=form)
        product = Product()
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        if form.image.data and form.image.data.filename:
            product.image_filename = save_image(form.image.data)
        db.session.add(product)
        db.session.commit()
        flash('Produk berhasil ditambahkan.', 'success')
        return redirect(url_for('product.index'))
    return render_template('product/create.html', form=form)

@product_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        if form.image.data and form.image.data.filename:
            if product.image_filename:
                old_path = os.path.join(UPLOAD_FOLDER, product.image_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)
            product.image_filename = save_image(form.image.data)
        db.session.commit()
        flash('Produk berhasil diperbarui.', 'success')
        return redirect(url_for('product.index'))
    return render_template('product/edit.html', form=form, product=product)

@product_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    if product.image_filename:
        old_path = os.path.join(UPLOAD_FOLDER, product.image_filename)
        if os.path.exists(old_path):
            os.remove(old_path)
    db.session.delete(product)
    db.session.commit()
    flash('Produk berhasil dihapus.', 'success')
    return redirect(url_for('product.index'))