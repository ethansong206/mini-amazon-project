from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .product import bp as product_bp
    app.register_blueprint(product_bp)

    from .seller import bp as seller_bp
    app.register_blueprint(seller_bp)

    from .savedproduct import bp as saved_bp
    app.register_blueprint(saved_bp)

    from .order import bp as orders_bp
    app.register_blueprint(orders_bp)

    from .purchase import bp as purchase_bp
    app.register_blueprint(purchase_bp)

    return app
