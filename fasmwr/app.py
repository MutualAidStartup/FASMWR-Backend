from flask import Flask
from routes.routes import fasmwr
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# Flask App
app = Flask(__name__)
CORS(app, support_credentials=True)

# Database
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Routing
app.register_blueprint(fasmwr)