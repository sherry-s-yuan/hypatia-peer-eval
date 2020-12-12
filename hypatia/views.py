from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Storer, Feedback
from .serializers import StorerSerializer, FeedbackSerializer
from django.http import HttpResponse
import json
import pprint

# Create your views here.


class StorerView(generics.CreateAPIView):
    queryset = Storer.objects.all()
    serializer_class = StorerSerializer

class FeedbackView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

def evaluator_view(request):
    feedback_view = FeedbackView()
    feedback_lst = feedback_view.queryset
    # doc_id_str = [feedback.doc_id for feedback in feedback_lst]
    original_author_id_str = [feedback.original_author_id.original_author_id for feedback in feedback_lst]
    editor_id_str = [feedback.editor_id for feedback in feedback_lst]
    feedback_correctness = [[feedback.feedback[key][1] for key in feedback.feedback] for feedback in feedback_lst]
    feedback_str = [[feedback.feedback[key][0] for key in feedback.feedback] for feedback in feedback_lst]
    feedback_score = [feedback.score for feedback in feedback_lst]
    # print(answer_str)
    context = {'queryset': []}
    for i in range(len(original_author_id_str)):
        original_author, editor = original_author_id_str[i], editor_id_str[i]
        scores = feedback_score[i]
        for j in range(len(feedback_correctness[i])):
            correct = feedback_correctness[i][j]
            feedback_string = feedback_str[i][j]
            context['queryset'].append({
                'original_author': original_author if j == 0 else '',
                'editor': editor if j == 0 else '',
                'feedback': feedback_string,
                'correctness': correct,
                'final_score': scores if j == len(feedback_correctness[i])-1 else ''
            })
    return render(request, "data_summary.html", context)

def home(request):
    feedback_view = FeedbackView()
    feedback_lst = feedback_view.queryset
    doc_id_str = [feedback.doc_id for feedback in feedback_lst]
    original_author_id_str = [feedback.original_author_id for feedback in feedback_lst]
    feedback_id = [[key for key in feedback.feedback] for feedback in feedback_lst]
    feedback_correctness = [[feedback.feedback[key][1] for key in feedback.feedback] for feedback in feedback_lst]
    feedback_str = [[feedback.feedback[key][0] for key in feedback.feedback] for feedback in feedback_lst]
    contain_error_str = [feedback.score for feedback in feedback_lst]
    # print(answer_str)
    return HttpResponse(feedback_str)


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

