from flask import *
from flask_login import current_user, login_required

from models.database import db
from models.user import User
from models.Item import Item
from models.CartItem import CartItem

cart = Blueprint('cart', __name__)


@cart.route('/addToCart/<int:item_id>/<int:user_id>')
@login_required
def addToCart(item_id, user_id):
    """Add an item to the cart"""
    new_item = CartItem(user_id=user_id, item_id=item_id)
    try:
        db.session.add(new_item)
        db.session.commit()
        flash('added successfully to cart', 'success')
    except:
        db.session.rollback()
        flash('Error adding new item', 'danger')
    return redirect(url_for('index'))


@cart.route('/cart', methods=['GET', 'POST'])
@login_required
def to_cart():
    """display items in the cart"""
    itemData = Item.query.filter(Item.id == CartItem.item_id and current_user.id == CartItem.user_id).all()
    count = CartItem.query.filter(Item.id == CartItem.item_id and current_user.id == CartItem.user_id).count()
    subtotal = 0
    for item in itemData:
        subtotal += item.price
    if count == 0:
        flash('No cart items available to purchase.', 'danger')
        return redirect(url_for('index'))
    return render_template('cart.html', itemData=itemData, subtotal=subtotal, count=count)


@cart.route('/removeFromCart')
def removeFromCart():
    """Route to  remove an item from the cart."""
    user_id = CartItem.query.filter(current_user.id == User.id).first()
    try:
        db.session.delete(user_id)
        db.session.commit()
        flash('Successfully removed item', 'success')
    except:
        flash('Error removing item')
    return redirect(url_for('cart.to_cart'))
