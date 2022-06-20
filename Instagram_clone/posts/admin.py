from django.contrib import admin

from posts.models import Posts, Comment

admin.site.register(Posts)
admin.site.register(Comment)
