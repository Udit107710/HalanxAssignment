from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Address(models.Model):
    street_address = models.TextField()
    city = models.CharField(max_length= 30)
    state = models.CharField(max_length= 30)
    pincode = models.IntegerField()
    country = models.CharField(max_length= 30)

class Profile(models.Model):
    GENDER_CHOICES = [ ('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user_profile')
    phone_no = models.BigIntegerField(unique=True, validators=[MaxValueValidator(9999999999),MinValueValidator(0000000000)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to= user_directory_path)
    date_of_birth = models.DateField()
    permanent_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name='permanent_address_is')
    street_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name= 'street_address_is')
    company_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name= 'company_address_is')
    friends = models.ManyToManyField(User, related_name= 'friends_are')

    def image_tag(self):
        return mark_safe('<img src="{0}" width="{1}" height="{2}">'.format(self.profile_pic.url, 150, 150))

