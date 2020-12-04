from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Storer, Feedback
from .serializers import StorerSerializer
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
    assignment = Storer(doc_id=load_data["docid"], original_author_id=load_data["userid"], answers=load_data["answers"], contains_error=load_data["contains_error"])
    feedback = Feedback(doc_id=assignment, original_author_id=assignment, editor_id=load_data["editor_id"],
                        feedback=load_data["feedback"], score=load_data["score"])
    assignment.save()
    feedback.save()
    return HttpResponse("Got save data request")

