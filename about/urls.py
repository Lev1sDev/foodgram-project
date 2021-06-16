from django.urls import path

from . import views

urlpatterns = [
    path('author/', views.AboutAuthorPage.as_view(), name='author'),
    path('tech/', views.AboutTechPage.as_view(), name='tech'),
]