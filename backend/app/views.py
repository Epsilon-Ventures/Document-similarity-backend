from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import numpy as np
# Create your views here.

def home(req):
    return HttpResponse("hello world")

def getData(req):
    data = {
        "name":"nitesh",
        "roll-number":"075bct058",
        "college":"pulchowk campus"
    }
    return JsonResponse (data)

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

    # print("response - ",response)
    # print("response.json - ", response.json())

    result = np.array(response.json())
    a = np.squeeze(result)
    b_shape = np.mean(a,axis = 0)
    # print(b_shape)
    print(b_shape.shape)

    return JsonResponse({"value":b_shape.shape},safe = False)

def getSecondModel(req):
    API_URL = "https://api-inference.huggingface.co/models/Nischal2015/models_sbert_v6"
    headers = {"Authorization": "Bearer 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"}
    payload = {
        "inputs": {
            "source_sentence": "That is a happy person",
            "sentences": [
                "That is a happy dog",
                "That is a very happy person",
                "Today is a sunny day"
            ]
        },
    }
    
    response = requests.post(API_URL, headers = headers, json = payload)
    print("response.json - ",response.json())
    return JsonResponse(response.json(), safe = False)


