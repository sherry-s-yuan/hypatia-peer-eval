from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Storer, Feedback, Classroom
from .serializers import StorerSerializer
from rest_framework.decorators import api_view
from django.http import HttpResponse
import json

# Create your views here.


class StorerView(generics.CreateAPIView):
    queryset = Storer.objects.all()
    serializer_class = StorerSerializer


def home(request):
    return HttpResponse('home')


def create_view(request):
    return StorerView.as_view()(request)


@csrf_exempt
def save_data(request):
    body = request.body.decode("utf-8")
    load_data = json.loads(body)
    classroom = Classroom(num_assignments=load_data["NumAssignments"], num_answers=load_data["NumAnswers"])
    classroom.save()
    return HttpResponse("Got save data request")

# @api_view(['GET', 'POST'])
# def doc_list(request):
#     if request.method == 'POST':
#         new_doc = JSONParser().parse(request)
#         doc_serializer = StorerSerializer(data=new_doc)
#         if doc_serializer.is_valid():
#             doc_serializer.save()
#             return JsonResponse(doc_serializer.data,
#                                 status=status.HTTP_201_CREATED)
#         return JsonResponse(doc_serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'GET':
#         docs = Storer.objects.all()
#         doc_id = request.GET.get('doc_id', None)
#         if doc_id is not None:
#             docs = docs.filter(doc_id__icontains=doc_id)
#         doc_serializer = StorerSerializer(docs, many=True)
#         return JsonResponse(doc_serializer.data, safe=False)
#
#
# @api_view(['GET', 'DELETE'])
# def doc_detail(request, doc_id):
#     doc = Storer.objects.get(pk=doc_id)
#     if request.method == "GET":
#         doc_serializer = StorerSerializer(doc)
#         return JsonResponse(doc_serializer.data)
#     elif request.method == 'DELETE':
#         doc.delete()
#         return JsonResponse({'message': 'Document was deleted'}, status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET'])
# def error_list(request):
#     error_docs = Storer.objects.filter(contains_error=True)
#
#     if request.method == 'GET':
#         docs_serializer = StorerSerializer(error_docs, many=True)
#         return JsonResponse(docs_serializer.data, safe=False)
