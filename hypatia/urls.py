from django.conf.urls import url
from django.urls import path
from .views import StorerView

urlpatterns = [
    path('', StorerView.as_view(), name='as_view')
]
