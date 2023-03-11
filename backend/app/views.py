from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

from pymilvus import Collection
from .milvus import pool
from .models import loaded_model as model
from .utils.helper_functions import prepare_response

# IMPORTS FOR THE TEST VIEW FILE UPLOADS    
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import FileSerializer
from io import BytesIO


@api_view(["POST","GET"])
def model_request(req):
    """Sends reponse to the frontend

    Args:
        req (dict): Dictionary containing the question and subject

    Returns:
        json: Json response containing the id, question, subject and similarity score
    """
    pool.connect()
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
        response_final = prepare_response(res,model,embeddings)
        return JsonResponse(response_final, safe = False)
    
@api_view(["POST"])
def add_question(req):
    """Adds question to the milvus database

    Args:
        req (dict): Dictionary containing the question and subject

    Returns:
        json: Json response containing the id, question, subject and similarity score
    """
    pool.connect()
    collection = Collection("questions")

    if req.method == 'POST':
        query_question = req.body.decode('utf-8')  

        input_query = json.loads(query_question)
        question = [input_query["question"]]
        embeddings = model.encode(question)
        collection.insert(
            [
                {
                    "question": input_query["question"],
                    "subject": input_query["subject"].lower(),
                    "embeddings": embeddings.tolist()
                }
            ]
        )
        return JsonResponse("Question added", safe = False)

#TEST VIEW FUNCTION FOR THE RETRIEVE OF FILE FROM THE BACKEND
class FileViewSet(viewsets.ViewSet):
    serializer_class = FileSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
            # do something with the file object
            print("file object - ",file_obj)

            # THIS WAY OF READING RETRIEVED FILE FINALLY WORKED . It is InMemoryUploadFile , so it is read this way
            file_content_ioByte = file_obj.read()
            
            # this is still in BytesIO format , to retrieve it in string format , we need to do this
            file_text_bytes = BytesIO(file_content_ioByte)
            
            # file_text is byte object , to convert that into string, we need to call .decode() function
            file_text_string = file_text_bytes.getvalue().decode()

            # to convert the string into list
            file_text_question_list = file_text_string.split("\n")
            print(file_text_question_list)


            return Response({'status': 'file uploaded'})
        else:
            return Response(serializer.errors, status=400)


