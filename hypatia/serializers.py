from rest_framework import serializers
from .models import Storer, Feedback


class StorerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storer
        fields = ('doc_id', 'original_author_id', 'answers', 'contains_error')


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storer
        fields = ('doc_id', 'original_author_id', 'editor_id', 'feedback', 'date_created', 'score')
