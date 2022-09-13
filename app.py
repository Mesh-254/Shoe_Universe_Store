from flask import *
from flask.cli import load_dotenv
from werkzeug.utils import secure_filename
import os

from blueprints.auth import auth
from blueprints.cart import cart
from blueprints.add import add
from blueprints.profile import profile
from blueprints.order import order
from blueprints.categories import category
from blueprints.About import about

from models.database import db
from models.Item import Item
from models.user import User
from models.UserTypes import UserType
from models.Category import Category
from models.CartItem import CartItem

from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
POSTS_PER_PAGE = 16

app = Flask(__name__, template_folder='./templates')
app.url_map.strict_slashes = False

# load environment variables
env = load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POSTS_PER_PAGE'] = POSTS_PER_PAGE
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.app = app
db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(cart, url_prefix='/')
app.register_blueprint(add, url_prefix='/')
app.register_blueprint(profile, url_prefix='/')
app.register_blueprint(order, url_prefix='/')
app.register_blueprint(category, url_prefix='/')
app.register_blueprint(about, url_prefix='/')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#
def getlogindetails():
    """Returns a list of user information"""
    email = User.query.get('email').first()
    if email not in session:
        loggedIn = False
        username = ''
        noOfItems = 0
    else:
        loggedIn = True
        username = User.query.get('username').filter_by(email=email).first()
        noOfItems = CartItem.query.get('item_id').filter_by(username=username).count()
    return loggedIn, username, noOfItems


@app.route('/base')
def base():
    username = User.query.get('username')
    return render_template('base.html', username=username)


@app.route('/')
def index():
    """displays index page"""
    page = request.args.get('page', 1, type=int)
    items = Item.query.paginate(page, app.config['POSTS_PER_PAGE'], False)
    categoryData = Category.query.all()
    return render_template('index.html', items=items, categoryData=categoryData)


@app.route('/static/images/<path:filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


def allowed_file(filename):
    """Check if a file is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/addItem', methods=['GET', 'POST'])
def add_item():
    """Add an item in the marketplace"""
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')

        image = request.files['image']
        if image.filename == '':
            flash('No selected file')
            return 'Image was not selected'
        if image and allowed_file(image.filename):
            # image.save(secure_filename(image.filename))
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image = filename

        new_item = Item(name=name, image=image, price=price, categoryId=category)
        categories = Category.query.all()
        try:
            db.session.add(new_item)
            db.session.commit()
            flash('Successfully created new item.', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Failed to create new item.', 'danger')
            return render_template('add.html', categories=categories)


@app.route('/remove/<int:item_id>')
@login_required
def removeItem(item_id):
    """Delete an item from the web app"""
    item = Item.query.filter(Item.id == item_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
