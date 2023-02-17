from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import numpy as np
from rest_framework.decorators import api_view
import json

from pymilvus import connections, Collection, utility
from sentence_transformers import SentenceTransformer




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



def database_connection(req):
    model = SentenceTransformer("Nischal2015/models_sbert_v6")

    endpoint="https://in01-48ca8867d6ebb85.aws-us-west-2.vectordb.zillizcloud.com:19536"
    connections.connect(
    uri=endpoint,
    secure=True,
    user='kamao',
    password='Random4545'
    )
    collection = Collection("questions")

    question = ['What is a handoff and what are some various handoff detection techniques?']


    embeddings = model.encode(question)
    search_params = {
        "metric_type": "L2",
        "params": {"level": 1},
    }
    output_fields = ["question1"]


    result = collection.search(
    data = embeddings.tolist(),
    anns_field="embeddings",
    param=search_params,
    limit=5,
    )

    ids = result[0].ids
    res = collection.query(
    expr = f"id in {ids}",   # id in [1, 3, 4, 5]
    output_fields=output_fields,
    consistency_level="Strong"
    )
    print(res)
    return JsonResponse(res, safe = False)

