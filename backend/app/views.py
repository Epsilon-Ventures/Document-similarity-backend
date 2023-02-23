from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import numpy as np
from rest_framework.decorators import api_view
import json

from pymilvus import connections, Collection, utility
from sentence_transformers import SentenceTransformer
from .utils.helper_functions import similarity_score_calculator

@api_view(["POST","GET"])
def model_request(req):
    model = SentenceTransformer("Nischal2015/models_sbert_v6")

    endpoint="https://in01-48ca8867d6ebb85.aws-us-west-2.vectordb.zillizcloud.com:19536"
    connections.connect(
    uri=endpoint,
    secure=True,
    user='kamao',
    password='Random4545'
    )
    collection = Collection("questions")

    if req.method == 'POST':

        query_question = req.body.decode('utf-8')  
        # question = ['What is a handoff and what are some various handoff detection techniques?']

        input_question = json.loads(query_question)
        question = [input_question["question"]]
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

        response_final = similarity_score_calculator(res,model,embeddings)
        return JsonResponse(response_final, safe = False)

