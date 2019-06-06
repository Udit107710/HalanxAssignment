from django.contrib import admin
from .models import Profile, Address
#from imagekit.admin import AdminThumbnail
class ProfileAdmin(admin.ModelAdmin):
    #image_display = AdminThumbnail(image_field='profile_pic')
    list_display = ('image_tag', 'user')
    list_filter = ('gender', )
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address)
