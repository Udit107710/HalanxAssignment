from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Profile
from .serializers import RegisterUserSerializer, LoginDetailSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer= RegisterUserSerializer(data= request.data)
        if serializer.is_valid():
            user= User.objects.create_user(serializer.validated_data['name'], serializer.validated_data['email'], serializer.validated_data['password'])
            user.save()
            profile = Profile(user= user, phone_no=serializer.data['phone_no'], gender=serializer.data['gender'], date_of_birth=serializer.data['date_of_birth'])
            profile.save()
            return Response("User registered! with id:" + str(user.id), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginDetailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username= username, password= password)
            if user is not None:
                login(user=user, request= request)
                return Response("LoggedIn!", status=status.HTTP_200_OK)
            else:
                return Response("User not found!", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response("Logged out!", status=status.HTTP_200_OK)
