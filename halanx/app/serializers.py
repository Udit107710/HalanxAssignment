from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class RegisterUserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone_no = serializers.IntegerField(max_value=9999999999, min_value= 111111111)
    password = serializers.CharField(style={'input_type': 'password'})
    gender = serializers.CharField(allow_null= True)
    date_of_birth = serializers.DateField(allow_null=True)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'profile')

class ProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs= {'user': { 'required': False},'friends': {'required': False} }

    def del_values(self, validated_data):
        validated_data.pop('name')
        validated_data.pop('email')
        validated_data.pop('password')
        
    #def create(self, validated_data):
    #    user = User.objects.create_user(validated_data['name'], validated_data['email'], validated_data['password'])
    #    user.save()
    #    validated_data.pop('name')
    #    validated_data.pop('email')
    #    validated_data.pop('password')
    #    profile = Profile(validated_data.values())
    #    profile.save()

