from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Storer, Feedback
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
    pass
#     body = request.body.decode("utf-8")
#     load_data = json.loads(body)
#     classroom = Classroom(num_assignments=load_data["NumAssignments"], num_answers=load_data["NumAnswers"])
#     classroom.save()
#     return HttpResponse("Got save data request")
