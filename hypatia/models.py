from django.db import models


# Create your models here.

class Storer(models.Model):
    original_author_id = models.IntegerField(primary_key=True, null=False)
    doc_id = models.CharField(max_length=8, null=True)
    answers = models.JSONField()
    contains_error = models.BooleanField(null=True)


class Feedback(models.Model):
    original_author_id = models.ForeignKey(Storer, on_delete=models.PROTECT,
                                           related_name=
                                           "%(class)s_author_id")
    doc_id = models.ForeignKey(Storer, null=True, on_delete=models.SET_NULL,
                               related_name="%(class)s_doc_id")
    editor_id = models.IntegerField(null=True)
    feedback = models.TextField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
