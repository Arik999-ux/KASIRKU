from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.category import Category
from app.forms.category_forms import CategoryForm

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories')
@login_required
def index():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('category/index.html', categories=categories)

@category_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category()
        category.name = form.name.data
        category.description = form.description.data
        db.session.add(category)
        db.session.commit()
        flash('Kategori berhasil ditambahkan.', 'success')
        return redirect(url_for('category.index'))
    return render_template('category/create.html', form=form)

@category_bp.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        existing = Category.query.filter_by(name=form.name.data).first()
        if existing and existing.id != category.id:
            flash('Nama kategori sudah digunakan.', 'danger')
            return render_template('category/edit.html', form=form, category=category)
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Kategori berhasil diperbarui.', 'success')
        return redirect(url_for('category.index'))
    return render_template('category/edit.html', form=form, category=category)

@category_bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    if category.products:
        flash('Kategori tidak bisa dihapus karena masih memiliki produk.', 'danger')
        return redirect(url_for('category.index'))
    db.session.delete(category)
    db.session.commit()
    flash('Kategori berhasil dihapus.', 'success')
    return redirect(url_for('category.index'))