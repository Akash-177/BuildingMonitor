from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    CORS(app)
    
    db.init_app(app)
    
    with app.app_context():
        from app import routes
        app.register_blueprint(routes.bp)
        
        # serve dashboard
        @app.route('/')
        def dashboard():
            return send_from_directory('../static', 'index.html')
        
        db.create_all()
    
    return app