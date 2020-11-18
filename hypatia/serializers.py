from rest_framework import serializers
from hypatia.models import Storer


class StorerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storer
        fields = ('doc_id',
                  'original_author_id',
                  'answers',
                  'contains_error')
