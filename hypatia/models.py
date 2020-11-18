from django.db import models


# Create your models here.

class Storer(models.Model):
    doc_id = models.CharField(max_length=8, primary_key=True, blank=False, default='')
    original_author_id = models.IntegerField(blank=False, default='')
    answers = models.JSONField()
    contains_error = models.BooleanField()
