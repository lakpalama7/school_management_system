from django.contrib import admin
from .models import School, Grade, Fee

# Register your models here.
admin.site.register(School)
admin.site.register(Grade)
admin.site.register(Fee)