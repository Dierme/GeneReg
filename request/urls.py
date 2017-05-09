from django.conf.urls import url

from . import views

app_name = 'request'
urlpatterns = [
    # ex: /request/
    url(r'^$', views.index, name='index')
]
