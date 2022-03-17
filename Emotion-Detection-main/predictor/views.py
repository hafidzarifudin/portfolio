from cgitb import text
import re
import json
from django.shortcuts import render

# Create your views here.
from .apps import PredictorConfig
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView
from . import preprocess

class detect_text(APIView):
    def post(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                text = body['text']
                if isinstance(text, str):
                    cleaning = preprocess.clean([text])
                    prediction = PredictorConfig.model.predict([cleaning])[0]
                    result = {'text': text, 'prediction': prediction}
                    respon = {'status': 200, 'message': 'OK', 'payload': result}
                    return JsonResponse(respon, safe=False)
            except Exception as e:
                error_response = {'status': 400, 'message': 'Error Occured: ' + str(e)}
                return JsonResponse(error_response)

class detect_list(APIView):
    def post(self, request):
        if request.method == 'POST':
            try:
                body = json.loads(request.body)
                text = body['text']
                if isinstance(text, list):
                    results_list = []
                    pred_results = []

                    for x in text:
                        cleaning = preprocess.clean([x])
                        prediction = PredictorConfig.model.predict([cleaning])[0]
                        pred_results.append(prediction)
                        results_list.append({
                            "text": x,
                            "emot_analysis": prediction,
                        })

                    sadness = 0
                    happy = 0
                    anger = 0
                    fear = 0
                    love = 0

                    for x in pred_results:
                        if x == 'sadness':
                            sadness += 1
                        elif x == 'happy':
                            happy += 1
                        elif x == 'anger':
                            anger += 1
                        elif x == 'fear':
                            fear += 1
                        elif x == 'love':
                            love += 1
                    
                    total = sadness + happy + anger + fear + love
                    sadness_total = sadness/total
                    happy_total = happy/total
                    anger_total = anger/total
                    fear_total = fear/total
                    love_total = love/total
                    percentage = {
                        "sadness": sadness_total,
                        "happy": happy_total,
                        "anger": anger_total,
                        "fear": fear_total,
                        "love": love_total,
                    }
                    
                    respon = {'status': 200, 'message': 'OK', 'payload': {'prediction': results_list, 'percentage': percentage}}

                    return JsonResponse(respon, safe=False)
            except Exception as e:
                error_response = {'status': 400, 'message': 'Error Occured: ' + str(e)}
                return JsonResponse(error_response)