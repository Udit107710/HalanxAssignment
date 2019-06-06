from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns= [
        path('register/', RegisterUserView.as_view()),
        path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
        path('login/', LoginView.as_view()),
        path('logout', LogoutView.as_view())
        ]
