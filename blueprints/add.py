from flask import Blueprint, url_for, render_template, request, flash
from flask import *
from flask_login import login_required

from models.database import db
from models.Category import Category
from models.Item import Item


add = Blueprint('add', __name__)


@add.route('/add')
@login_required
def admin_add():
    """Add a new item to the database"""
    categories = Category.query.all()
    return render_template('add.html', categories=categories)


@add.route('/remove')
@login_required
def remove():
    """Remove an item in the marketplace"""
    data = Item.query.filter_by(Item.id)
    return render_template('remove.html', data=data)


@add.route('/removeItem')
def remove_item():
    """Remove an item in the marketplace"""
    item_id = request.args.get('Item.id')
    try:
        item_id = Item.query.filter(Item.id == item_id).first()
        db.session.delete(item_id)
        db.session.commit()
        flash('Successfully removed item', 'success')
    except:
        flash('Failed to remove item.', 'danger')
        return redirect(url_for('/remove'))
    return redirect(url_for('/remove'))


@add.route('/category')
@login_required
def category():
    return render_template('addcategory.html')


@add.route('/addCategory', methods=['POST'])
def addCategory():
    """Add a new category to the database"""
    if request.method == 'POST':
        name = request.form.get('name')

        new_category = Category(name=name)
        old_category = Category.query.filter(Category.name == name).first()
        try:
            db.session.add(new_category)
            db.session.commit()
            flash('Added new category', 'success')
            return redirect('/')
        except:
            if old_category:
                flash('Error adding category', 'error')
                return "That category already exists. Please try again"
                return redirect(url_for('/category'))
