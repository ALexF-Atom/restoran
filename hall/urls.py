from django.urls import path

from . import views

urlpatterns = [
path('', views.IndexView.as_view(), name='index'),
path('<str:date>', views.TablesView.as_view(), name='tables-view'),
]
