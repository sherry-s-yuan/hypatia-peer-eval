from django.conf.urls import url
from hypatia import views

urlpatterns = [
    url(r'^api/hypatia$', views.doc_list),
    url(r'^api/hypatia/(?P<pk>[0-9]+)$', views.doc_detail),
    url(r'^api/hypatia/has_error$', views.error_list)
]
