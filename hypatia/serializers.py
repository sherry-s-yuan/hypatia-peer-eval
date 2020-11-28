from rest_framework import serializers
from .models import Storer


class StorerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storer
        fields = ('original_author_id', 'doc_id', 'answers', 'contains_error')
