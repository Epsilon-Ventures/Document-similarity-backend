from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import numpy as np
from rest_framework.decorators import api_view
import json


def home(req):
    return HttpResponse("hello world")

def getData(req):
    data = {
        "name":"nitesh",
        "roll-number":"075bct058",
        "college":"pulchowk campus"
    }
    return JsonResponse (data)

@api_view(['GET', 'POST'])
def getModelResponse(req):
    payload = {
        "input":'Today is a sunny day and Ill get some ice cream.'
    }

    payload1 = "Blue sounded too cold at the time and yet it seemed to work for gin"

    API_URL = "https://api-inference.huggingface.co/models/Nischal2015/models_sbert_gpl"
    
    headers = {
        "Authorization":"Bearer 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"
    }

    response = requests.post(API_URL, headers = headers, json = payload1)

    result = np.array(response.json())
    a = np.squeeze(result)
    b_shape = np.mean(a,axis = 0)
    # print(b_shape)
    print(b_shape.shape)

    return JsonResponse({"value":b_shape.shape},safe = False)

@api_view(['GET', 'POST'])
def getSecondModel(req):
    if req.method == "POST":
        data = json.loads(req.body.decode())
        print(data['text'])
   
        API_URL = "https://api-inference.huggingface.co/models/Nischal2015/models_sbert_v6"
        headers = {"Authorization": "Bearer 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"}
        payload = {
            "inputs": {
                "source_sentence": data["text"],
                "sentences": [
                    "Random guy am running a company",
                    "I run everyday in the morning",
                    "He runs my company"
                ]
            },
        }

        response = requests.post(API_URL, headers = headers, json = payload)
        print("response.json - ",response.json())
        return JsonResponse(response.json(), safe = False)
    return HttpResponse("not post request")






