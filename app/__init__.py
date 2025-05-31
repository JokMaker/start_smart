from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
    from app.routes.auth import auth as auth_blueprint
    from app.routes.jobs import jobs as jobs_blueprint
    from app.routes.mentorship import mentorship as mentorship_blueprint
    from app.routes.startups import startups as startups_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(jobs_blueprint)
    app.register_blueprint(mentorship_blueprint)
    app.register_blueprint(startups_blueprint)
    
    return app