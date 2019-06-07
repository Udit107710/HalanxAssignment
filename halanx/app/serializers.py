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

class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields = ('username','email')

class ProfileSerializer(serializers.ModelSerializer):
    permanent_address= AddressSerializer(required=False)
    company_address= AddressSerializer(required=False)
    street_address= AddressSerializer(required=False)
    user = UserSerializer(required=False)
    friends = FriendSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {'phone_no': {'required': False}, 
                        'gender': { 'required': False}, 
                        'profile_pic': {'required': False},
                        'date_of_birth': {'required': False}
                        }      

class RegisterUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'date_of_birth', 'gender', 'phone_no')
        
    def create(self, validated_data):    
        user_data= validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        Profile.objects.create(user=user,**validated_data)
        return user

class UpdateFriendSerializer(serializers.Serializer):
    username= serializers.CharField()
    email= serializers.EmailField()

class UpdateFriendsSerializer(serializers.Serializer):
    add = UpdateFriendSerializer(many=True, allow_null=True)
    remove = UpdateFriendSerializer(many=True, allow_null=True)


class UpdateUserSerializer(ProfileSerializer):
    GENDER_CHOICES= [('M', 'Male'), ('F', 'Femaile'), ('O', 'Others') ]

    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True,allow_blank=True, allow_null=True)
    date_of_birth = serializers.DateField(required= True, allow_null=True)
    permanent_address = AddressSerializer(required=True, allow_null=True)
    company_address = AddressSerializer(required=True, allow_null=True)
    street_address = AddressSerializer(required=True, allow_null=True)
    phone_no = serializers.CharField(max_length=10, min_length=10, required=True, allow_blank=True, allow_null=True)
    profile_pic = serializers.ImageField(required=False, allow_null=True)
    friends = UpdateFriendsSerializer(required=True)
    user = UserSerializer(required=True, allow_null=True)

    def update(self, instance, validated_data):
        print(validated_data)
        if validated_data['user'] is not None:
            user = User.objects.get(username= validated_data['user']['username'])
            user.email = validated_data['user']['email']
            user.set_passowrd(validated_data['user']['password'])
            user.save()

        if validated_data['friends']['add'] is not None:
            for users in validated_data['friends']['add']:
                instance.friends.add(User.objects.get(username=users['username']))
        else:
            instance.freinds = None
        if validated_data['friends']['remove'] is not None:
            for users in validated_data['friends']['remove']:
                instance.friends.remove(User.objects.get(username=users['username']))
        else:
            instance.friends = None

        permanent_address= validated_data['permanent_address']
        company_address= validated_data['company_address']
        street_address= validated_data['street_address']

        if permanent_address is not None:
            address_serializer = AddressSerializer(data= permanent_address)
            if address_serializer.is_valid():
                permanent_address_obj= address_serializer.save()
                instance.permanent_address= permanent_address_obj
            else:
                raise Exception(address_serializer.errors)
        else:
            instance.permanent_address= None

        if company_address is not None:
            address_serializer = AddressSerializer(data= company_address)
            if address_serializer.is_valid():
                company_address_obj = address_serializer.save()
                instance.company_address= company_address_obj
            else:
                raise Exception(address_serializer.errors)
        else:
            instance.company_address= None

        if street_address is not None:
            address_serializer = AddressSerializer(data= street_address)
            if address_serializer.is_valid():
                street_address_obj = address_serializer.save()
                instance.street_address= street_address_obj
            else:
                raise Exception(address_serializer.errors)
        else:
            instance.street_address= None

        instance.gender= validated_data['gender']
        instance.date_of_birth = validated_data['date_of_birth']
        instance.phone_no= validated_data['phone_no']
        instance.profile_pic= validated_data['profile_pic']
        instance.save()
        return instance

