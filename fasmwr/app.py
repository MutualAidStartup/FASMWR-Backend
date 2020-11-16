from flask import Flask
from routes.routes import fasmwr

app = Flask(__name__)

app.register_blueprint(fasmwr)