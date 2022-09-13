from flask import *
from models.Item import Item
from models.Category import Category

category = Blueprint('category', __name__)


@category.route('/itemDescription/<int:item_id>')
def itemDescription(item_id):
    """Item description route"""
    itemData = Item.query.filter(Item.id == item_id).first()
    return render_template('itemDescription.html', itemData=itemData)


@category.route('/men')
def men():
    """
    :return: route to men products
    """
    categoryName = Category.query.filter(Category.id == '2').first()
    items = Item.query.filter(Item.categoryId == '2').all()
    return render_template('men.html', items=items, categoryName=categoryName)


@category.route('/women')
def women():
    """
    :return: route to '/women' products
    """
    categoryName = Category.query.filter(Category.id == '1').first()
    items = Item.query.filter(Item.categoryId == '1').all()
    return render_template('women.html', items=items, categoryName=categoryName)
