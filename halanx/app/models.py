from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
#from django.dispatch import receiver
#from django.db.models.signals import post_save

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Address(models.Model):
    street_address = models.TextField()
    city = models.CharField(max_length= 30)
    state = models.CharField(max_length= 30)
    pincode = models.IntegerField()
    country = models.CharField(max_length= 30)

    def __str__(self):
        return self.city

class Profile(models.Model):
    GENDER_CHOICES = [ ('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user_profile')
    phone_no = models.BigIntegerField(unique=True, validators=[MaxValueValidator(9999999999),MinValueValidator(1000000000)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    profile_pic = models.ImageField(upload_to= user_directory_path,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    permanent_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name='permanent_address_is', null=True, blank=True)
    street_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name= 'street_address_is', null=True, blank=True)
    company_address = models.OneToOneField(Address, on_delete= models.CASCADE, related_name= 'company_address_is',null=True, blank=True)
    friends = models.ManyToManyField(User, related_name= 'friends_are', null=True, blank=True)

    def image_tag(self):
        if self.profile_pic:
            return mark_safe('<img src="{0}" width="{1}" height="{2}" >'.format(self.profile_pic.url, 150, 150))
        else:
            return mark_safe('<img src="" width="150" height="150" alt="Picture not uplaoded">')
