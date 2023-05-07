from django.contrib import admin
from .models import Subscriber, Category, Tags, Writer, Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('name','category','date')

# Register your models here.
admin.site.register(Subscriber)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Writer)
admin.site.register(Blog,BlogAdmin)