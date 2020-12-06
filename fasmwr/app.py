from flask import Flask
from flask_bcrypt import Bcrypt
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
bcrypt = Bcrypt()

# Routing
from routes.routes import fasmwr
from routes.user import users

app.register_blueprint(fasmwr)
app.register_blueprint(users)


if __name__ == '__main__':
    app.run()