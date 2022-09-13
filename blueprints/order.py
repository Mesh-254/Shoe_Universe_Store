from flask import Blueprint, render_template

order = Blueprint('order', __name__)


@order.route('/checkout')
def checkout():
    return render_template('checkout.html')

@order.route('/ordercomplete')
def ordercomplete():
    return render_template('order-complete.html')

