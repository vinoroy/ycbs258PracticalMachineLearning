from flask import Flask
from config import Config

from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

app.config.from_object(Config)

from app import routes