from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.travels_add),
    url(r'^add_trip$', views.add_trip),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^logout$', views.logout),
    url(r'^travels/join/(?P<id>\d+)$', views.join),
]

