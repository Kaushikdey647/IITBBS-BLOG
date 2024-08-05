from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flaskblog.config import Config

db = SQLAlchemy()
migration = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view="users.login"
login_manager.login_message_category="info"
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the migration
    migration.init_app(app,db)
    # Initialize the database
    db.init_app(app)
    # Initialize the bcrypt
    bcrypt.init_app(app)
    # Initialize the login manager
    login_manager.init_app(app)
    # Initialize the mail
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app