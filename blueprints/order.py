from flask import *
from flask_login import current_user
from models.CartItem import CartItem
from models.Item import Item

order = Blueprint('order', __name__)


@order.route('/checkout')
def checkout():
    itemData = Item.query.filter(Item.id == CartItem.item_id and current_user.id == CartItem.user_id).all()
    subtotal = 0
    for item in itemData:
        subtotal += item.price
    return render_template('checkout.html', itemData=itemData, subtotal=subtotal)


@order.route('/ordercomplete')
def ordercomplete():
    return render_template('order-complete.html')
