from flask import Flask

app = Flask(__name__)

'''
from tensorflow import keras
import pickle
rap_model = keras.models.load_model('app\ML_models/rap_model.h5')
indices_word = pickle.load(open('app\ML_models/indices_word.pkl','rb'))
word_indices = pickle.load(open('app\ML_models/word_indices.pkl','rb'))
'''

from app import routes


