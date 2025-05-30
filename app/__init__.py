from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder='static')

    # Load default config
    app.config.from_object('config.Config')

    # Load config from instance folder (if exists)
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to auth.login if not logged in

    # Import models
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints
    from .routes import bp as main_bp
    from .auth import auth as auth_bp

    # Register blueprints inside the create_app function
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app



# This function creates and configures the Flask application.
# It initializes the database and migration extensions, loads configuration settings,
# and registers the main blueprint for routing.
# The application is set up to use SQLAlchemy for database interactions and Flask-Migrate for handling database migrations.
# The create_app function is typically used in Flask applications to allow for
# easier testing and configuration management by creating an application instance with specific settings.
# The application instance can then be run or tested as needed.