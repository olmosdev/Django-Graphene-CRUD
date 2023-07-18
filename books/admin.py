from django.contrib import admin
from .models import Book

# Register your models here.
# Adding a model to be used in the the admin panel
# User: digamaol Password: password
admin.site.register(Book)