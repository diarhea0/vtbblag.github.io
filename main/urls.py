from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_index_view, name='main_index')
]
