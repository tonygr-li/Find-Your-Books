from django.contrib import admin
from .models import Post, Images

# Register your models here.
admin.site.register([Post, Images])