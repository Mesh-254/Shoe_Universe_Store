from flask import *

about = Blueprint('about', __name__)


@about.route('/about')
def about_page():
    """"About page"""
    return render_template('about.html')


@about.route('/contact/')
def contact():
    """Contact page"""
    return render_template('contact.html')

