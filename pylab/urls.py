from django.conf.urls import url

from . import views

app_name = 'pylab'
urlpatterns = [
    # ex: /request/
    url(r'^$', views.index, name='index'),
    url(r'^random/', views.random),
    url(r'^create/', views.create),
    url(r'^delete/', views.delete)
]
