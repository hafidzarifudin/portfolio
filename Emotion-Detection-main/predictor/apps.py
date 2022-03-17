from django.apps import AppConfig
from django.conf import settings
import os
import pickle


class PredictorConfig(AppConfig):
    #create path to models
    path = os.path.join(settings.MODELS, 'emotion_detection_model.p')

    #load models into seperate variables
    with open(path, 'rb') as pickled:
        data = pickle.load(pickled)
    model = data['model']

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'
