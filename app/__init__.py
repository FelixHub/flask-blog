from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from tensorflow import keras
import pickle

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

rap_model = keras.models.load_model('app\ML_models/rap_model.h5')
indices_word = pickle.load(open('app\ML_models/indices_word.pkl','rb'))
word_indices = pickle.load(open('app\ML_models/word_indices.pkl','rb'))

from app import routes, models


