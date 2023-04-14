from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'comment', 'created_at')



# Register your models here.
admin.site.register(Video)
admin.site.register(Comment, CommentAdmin)