from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.RegistrationAPIView.as_view()),
    path('authorization/', views.AuthorizationAPIView.as_view()),
    path('confirm/', views.ConfirmationAPIView.as_view()),
    # path('api/v1/directors/<int:id>/', views.directors_detail_api_view),
]