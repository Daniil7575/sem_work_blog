from django.contrib import admin

from .models import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_image', 'date_of_birth', 'user')
    list_editable = ('date_of_birth', 'user')


admin.site.register(Profile, ProfileAdmin)
