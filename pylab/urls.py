from django.conf.urls import url

from . import views

app_name = 'pylab'
urlpatterns = [
    # ex: /request/
    url(r'^$', views.index, name='index')
]
