from django.db import models


# Create your models here.

class Storer(models.Model):
    doc_id = models.CharField(max_length=11, primary_key=True, null=False)
    original_author_id = models.IntegerField(default='', null=True)
    answers = models.JSONField()
    contains_error = models.BooleanField(null=True)

    objects = models.Manager()


class Feedback(models.Model):
    doc_id = models.ForeignKey(Storer, null=False, on_delete=models.PROTECT,
                               related_name="%(class)s_doc_id")
    original_author_id = models.ForeignKey(Storer, on_delete=models.CASCADE,
                                           related_name="%(class)s_author_id")
    editor_id = models.IntegerField(null=True)
    feedback = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True)
    objects = models.Manager()
