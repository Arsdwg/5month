from django.urls import path
from . import views


urlpatterns = [
    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorItemAPIView.as_view()),
    path('movies/', views.MovieListAPIView.as_view()),
    path('movies/<int:id>/', views.MovieItemAPIView.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewItemAPIView.as_view()),
]