from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, RetrieveProfileView, UpdateProfileView, FetchProfileView
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_exempt

urlpatterns= [
        path('register/', RegisterUserView.as_view()),
        path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
        path('login/', LoginView.as_view()),
        path('logout', LogoutView.as_view()),
        path('retrieve/', RetrieveProfileView.as_view(), name='retrieve_user_info'),
        path('update/', UpdateProfileView.as_view()),
        path('fetch-users', FetchProfileView.as_view() )
        ]
