from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from .utils.helper_functions import similarity_score_calculator
import os

@api_view(["POST","GET"])
def model_request(req):
    model = SentenceTransformer("Nischal2015/sbert_eng_ques")

    endpoint="https://in01-a634cdb85f99794.aws-us-west-2.vectordb.zillizcloud.com:19542"
    connections.connect(
        uri=endpoint,
        secure=True,
        user=os.environ.get('DB_NAME'),
        password=os.environ.get('DB_PASSWORD')
    )
    collection = Collection("questions")

    if req.method == 'POST':
        query_question = req.body.decode('utf-8')  

        input_query = json.loads(query_question)
        question = [input_query["question"]]
        embeddings = model.encode(question)
        search_params = {
            "metric_type": "IP",
            "params": {"level": 1},
        }
        output_fields = ["question", "subject"]

        result = collection.search(
            data = embeddings.tolist(),
            anns_field="embeddings",
            param=search_params,
            limit=5,
            expr=None if input_query['subject'] == "" else f"subject == \"{input_query['subject'].lower()}\""
        )

        ids = result[0].ids
        res = collection.query(
        expr = f"id in {ids}",   # id in [1, 3, 4, 5]
        output_fields=output_fields,
        consistency_level="Strong"
        )

        response_final = similarity_score_calculator(res,model,embeddings)
        return JsonResponse(response_final, safe = False)

