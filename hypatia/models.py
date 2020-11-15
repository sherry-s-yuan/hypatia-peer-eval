from django.db import models


# Create your models here.

class Storer(models.Model):
    doc_id = models.CharField(max_length=8, primary_key=True)
    original_author_id = models.IntegerField()
    answers = models.JSONField()
    contains_error = models.BooleanField()
