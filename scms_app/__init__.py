from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

# Extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
    app.config['JWT_SECRET_KEY'] = 'supersecret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Home Route (optional)
    @app.route('/')
    def home():
        return render_template('index.html')  # Make sure templates/index.html exists

    # Register Blueprints
    from scms_app.routes.auth import auth_bp
    from scms_app.routes.complaints import complaint_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(complaint_bp, url_prefix='/complaints')

    return app
