from django.conf.urls import url
from django.urls import path
from .views import home, create_view
from .views import save_data

urlpatterns = [
    # path('', StorerView.as_view(), name='as_view')
    path("", home, name="go_to_home"),
    path("basic_view", create_view, name="basic_view"),
    path("save", save_data, name="save")
]
