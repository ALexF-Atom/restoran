from django.urls import path

from .views import IndexView, RestoranDetailView, HallDetailView


urlpatterns = [
    path('', IndexView.as_view()),
    path('<str:name>', RestoranDetailView.as_view(), name='restoran'),
    path('<str:slug>/<str:date>', HallDetailView.as_view(), name='hall'),
]
