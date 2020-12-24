from django.urls import path
from .views import (IndexView,
                    RestoranDetailView, CreateSchemeView,
                    UpdateSchemeView, DeleteSchemeView)

from django.contrib.auth import views as a_views

urlpatterns = [
    path('',
         IndexView.as_view()),
    path('<str:name>',
         RestoranDetailView.as_view(), name='radmin_restoran'),
    path('update-scheme/<str:slug>',
         UpdateSchemeView.as_view(), name='update_scheme'),
    path('create-scheme/<str:name>',
         CreateSchemeView.as_view(), name='create_scheme'),
    path('delete-scheme/<str:slug>',
         DeleteSchemeView.as_view(), name='delete'),
    path('staff/login/',
         a_views.LoginView.as_view(template_name='radmin/login.html')),
    path('logout/',
         a_views.LogoutView.as_view(next_page='/'), name='logout'),
]
