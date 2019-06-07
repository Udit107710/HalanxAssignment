from rest_framework import serializers
from .models import Profile, Address
from django.contrib.auth.models import User

class LoginDetailSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model= Address
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    permanent_address= AddressSerializer()
    company_address= AddressSerializer()
    street_address= AddressSerializer()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class RegisterUserSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'phone_no', 'gender', 'date_of_birth')

    def create(self, validated_data):
        user_data= validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user,**validated_data)
        return user
