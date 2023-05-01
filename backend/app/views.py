from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

import numpy as np
from datetime import date

from sentence_transformers.util import cos_sim

from pymilvus import Collection
from .milvus import pool
from .models import loaded_model as model
from .utils.helper_functions import prepare_response, search_query
from .utils.file_upload import file_upload_embeddings

# IMPORTS FOR THE TEST VIEW FILE UPLOADS    
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import TwoFileSerializer, FileSerializer, TopTwoQuestionSerializer
from io import BytesIO


@api_view(["POST","GET"])
def model_request(req):
    """Sends response to the frontend

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
        output_fields = ["question", "subject", "year", "sem"]

        result = collection.search(
            data = embeddings.tolist(),
            anns_field="embeddings",
            param=search_params,
            limit=5,
            expr=None if input_query['subject'] == "" else f"subject == \"{input_query['subject'].lower()}\""
        )

        for item in result:
            res = search_query(item, collection, output_fields)
                    
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
    collection = Collection("dummy_questions")

    if req.method == 'POST':
        query_question = req.body.decode('utf-8')  

        input_query = json.loads(query_question)
        subject = input_query["subject"]
        year = input_query["year"]
        sem = input_query["sem"]  
        payload = input_query["payload"]   
        
        questions = [value['question'] for value in payload]
        marks = [value['mark'] for value in payload]
        subjects = [subject for _ in range(len(questions))]
        years = [year for _ in range(len(questions))]
        sems = [sem for _ in range(len(questions))]
        embeddings = model.encode(questions)
        paper_ids = ["0" for _ in range(len(questions))]

        collection.insert([
            embeddings,
            subjects,
            years,
            sems,
            questions,
            paper_ids,
            marks
        ])
        return JsonResponse([questions,subjects,sems,years], safe = False)
#TEST VIEW FUNCTION FOR THE RETRIEVE OF FILE FROM THE BACKEND
class FileViewSet(viewsets.ViewSet):
    serializer_class = FileSerializer
    ques_list = []

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']

            embeddings = file_upload_embeddings(FileViewSet, file_obj)

            pool.connect()
            collection = Collection("questions")

            search_params = {
                "metric_type": "IP",
                "params": {"level": 1},
            }
            output_fields = ["question", "subject", "year", "sem"]

            result = collection.search(
                data = embeddings.tolist(),
                anns_field="embeddings",
                param=search_params,
                limit=5,
            )
            list_of_responses = []
            for item in result:
                res = search_query(item, collection, output_fields)
                response = prepare_response(res,model,embeddings)
                list_of_responses.append(response)

            return JsonResponse(list_of_responses, safe = False)
        else:
            return Response(serializer.errors, status=400)
        
    def get(self, request):
        return JsonResponse(FileViewSet.ques_list, safe = False)

class TwoFileViewSet(viewsets.ViewSet):
    serializer_class = TwoFileSerializer
    ques_list1 = []
    ques_list2 = []

    def get(self,req):
        return JsonResponse("you reached this route",safe=False)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file_obj1 = serializer.validated_data['file1']
            file_obj2 = serializer.validated_data['file2']

            # THIS WAY OF READING RETRIEVED FILE FINALLY WORKED . It is InMemoryUploadFile , so it is read this way
            file_content_ioByte1 = file_obj1.read()
            file_content_ioByte2 = file_obj2.read()
            
            # # this is still in BytesIO format , to retrieve it in string format , we need to do this
            file_text_bytes1 = BytesIO(file_content_ioByte1)
            file_text_bytes2 = BytesIO(file_content_ioByte2)
            
            # # file_text is byte object , to convert that into string, we need to call .decode() function
            file_text_string1 = file_text_bytes1.getvalue().decode()
            file_text_string2 = file_text_bytes2.getvalue().decode()

            # # to convert the string into list
            file_text_question_list1 = file_text_string1.split("\n")
            file_text_question_list2 = file_text_string2.split("\n")

            file_text_question_list1 = [item for item in file_text_question_list1 if item != ""]
            file_text_question_list2 = [item for item in file_text_question_list2 if item != ""]

            # print(file_text_question_list1)

            TwoFileViewSet.ques_list1 = file_text_question_list1
            TwoFileViewSet.ques_list2 = file_text_question_list2

            # convert to embeddings
            embeddings1 = model.encode(file_text_question_list1)
            embeddings2 = model.encode(file_text_question_list2)
            
            # calculating mean 
            emb1_mean = np.mean(embeddings1,axis=0) 
            emb2_mean = np.mean(embeddings2,axis=0)
            two_file_similarity = cos_sim(emb1_mean,emb2_mean)

            return JsonResponse(two_file_similarity.tolist(),safe=False)

        
    def get(self, request):
        print(TwoFileViewSet.ques_list1)
        return JsonResponse({"file1":TwoFileViewSet.ques_list1,"file2":TwoFileViewSet.ques_list2}, safe = False)

class TopTwoQuestion(viewsets.ViewSet):
    serializer_class = TopTwoQuestionSerializer
    ques_list = []
    def create(self, request):
        subject = request.data['subject']

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            file_obj = serializer.validated_data['file']
        
            embeddings = file_upload_embeddings(TopTwoQuestion, file_obj)

            pool.connect()
            collection = Collection("questions")

            search_params = {
                "metric_type": "IP",
                "params": {"level": 1},
            }
            output_fields = ["question", "subject", "year", "sem"]

            # current_year = date.today().year
            # current = str(current_year)
            # past = str(current_year - 1)
            current = 2013
            past= 2012

            result = collection.search(
                data = embeddings.tolist(),
                anns_field="embeddings",
                param=search_params,
                limit=2,
                expr = f"subject == \"{subject.lower()}\" && year in [\"{current}\", \"{past}\"]"
            )

            list_of_responses = []
            for item in result:
                res = search_query(item, collection, output_fields)
                response = prepare_response(res,model,embeddings)
                list_of_responses.append(response)

            return JsonResponse(list_of_responses, safe = False)
