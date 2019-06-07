from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Profile
from .serializers import RegisterUserSerializer, LoginDetailSerializer, ProfileSerializer

class RegisterUserView(APIView):
    def post(self, request):
        serializer= RegisterUserSerializer(data= request.data)
        if serializer.is_valid():
            user= serializer.save()
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

class RetrieveProfileView(APIView):
    def get(self,request):
        print(request.user)
        if request.user.is_authenticated:
            #profile = User.objects.all().select_related('custom_user_profile').get(id= request.user.id)
            profile= Profile.objects.get(user= request.user)
            print(profile)
            serializer = ProfileSerializer(profile)
            #serializer.data['name'] = request.user.username
            #serializer.data['email'] = request.user.email
            #serializer.data['password'] = request.user.password
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Authentication required", status=status.HTTP_403_FORBIDDEN)
