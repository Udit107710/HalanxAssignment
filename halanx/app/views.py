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
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication

from .models import Profile, Address
from .serializers import UpdateUserSerializer, RegisterUserSerializer, ProfileSerializer, LoginDetailSerializer, AddressSerializer, AllProfilesSerializer, FilterSerializer

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
            serializer = UpdateUserSerializer(profile, data= request.data)
            if serializer.is_valid():
                serializer.save()

                return redirect('retrieve_user_info')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Authentication required", status=status.HTTP_403_FORBIDDEN)

class FetchProfileView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = FilterSerializer(data= request.data)
            if serializer.is_valid():
                user_profile= Profile.objects.get(user= request.user)
                list_of_profiles= []
                print(serializer.data)
                if serializer.data['gender'] is not None:
                    profile_objects= Profile.objects.filter(gender= serializer.data['gender'] ).select_related('permanent_address').select_related('user').all()
                else:
                    profile_objects= Profile.objects.select_related('permanent_address').all()

                for profile in profile_objects:
                    if serializer.data['permanent_address_city'] is not None:
                        if profile.permanent_address is not None: 
                            if profile.permanent_address.city == serializer.data['permanent_address_city']:
                                self.append_profiles(user_profile, profile, list_of_profiles, request)
                    else:
                        self.append_profiles(user_profile,profile,list_of_profiles, request)
                    
                return Response(list_of_profiles, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Authentication Required!", status=status.HTTP_403_FORBIDDEN)

    def append_profiles(self,user_profile, profile, list_of_profiles, request):
        #print(profile.profile_pic)
        if user_profile.friends is not None:
            if profile.user_id in user_profile.friends.all():
                is_person_my_friend= 'Yes'
            else:
                is_person_my_friend= 'No'

            if profile.friends is not None:
                count_of_mutual_friends= len(list(set(profile.friends.all()).intersection(user_profile.friends.all())))
            else:
                count_of_motual_friends= 0
        else:
            is_person_my_friend= "No"
            count_of_mutual_friends= 0

        user_id= profile.user.id
        name= profile.user.username
        gender= profile.gender
        try:
            profile_pic_url= request.build_absolute_uri(profile.profile_pic.url)
        except ValueError:
            profile_pic_url= None
        if profile.permanent_address is not None:
            profile_serializer= AllProfilesSerializer(data={'user_id': user_id, 'name': name, 'gender': gender, 'profile_pic_url': profile_pic_url, 'is_person_my_friend': is_person_my_friend, 'count_of_mutual_friends': count_of_mutual_friends, 'permanent_address_city': profile.permanent_address.city})
        else:
            profile_serializer= AllProfilesSerializer(data={'user_id': user_id, 'name': name, 'gender': gender, 'profile_pic_url': profile_pic_url, 'is_person_my_friend': is_person_my_friend, 'count_of_mutual_friends': count_of_mutual_friends, 'permanent_address_city': None})

        if profile_serializer.is_valid():
            list_of_profiles.append(profile_serializer.data)
        else:
            print(profile_serializer.errors)
