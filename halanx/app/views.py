from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import SessionAuthentication

from .models import Profile
from .serializers import UpdateUserSerializer, RegisterUserSerializer, ProfileSerializer, LoginDetailSerializer, AddressSerializer

class RegisterUserView(APIView):
    #authentication_classes = []
    def post(self, request):
        serializer= RegisterUserSerializer(data= request.data)
        if serializer.is_valid():
            user= serializer.save()
            return Response("User registered! with id:" + str(user.id), status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    #authentication_classes = []
    def post(self, request):
        serializer = LoginDetailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request=request, username= username, password= password)
            if user is not None:
                login(user=user, request= request)
                return Response("Logged in!", status=status.HTTP_200_OK)
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
        if request.user.is_authenticated:
            profile= Profile.objects.get(user= request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Authentication required", status=status.HTTP_403_FORBIDDEN)

class UpdateProfileView(APIView):
    #authentication_classes= []
    def post(self, request):
        parser_classes = (JSONParser,)
        if request.user.is_authenticated:
            profile = Profile.objects.get(user= request.user)
            print(profile)
            serializer = UpdateUserSerializer(profile, data= request.data)
            if serializer.is_valid():
                serializer.save()

                return redirect('retrieve_user_info')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Authentication required", status=status.HTTP_403_FORBIDDEN)
