__author__ = 'Tusfiqur'
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'update_table_data/$', views.update_table_data, name="update_data"),
    url(r'^(?P<data_id>[0-9]+)/(?P<table_name>[a-z_]+)/delete_data/$', views.delete_data, name="delete_data"),

]

