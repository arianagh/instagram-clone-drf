from django.contrib import admin

from account.models import Profile, FollowerTable, FollowerUser

admin.site.register(Profile)
admin.site.register(FollowerTable)
admin.site.register(FollowerUser)
