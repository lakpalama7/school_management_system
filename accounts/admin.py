from django.contrib import admin
from .models import CustomUser, OTP
# Register your models here.
admin.site.register(CustomUser)

class OTPAdmin(admin.ModelAdmin):
    list_display = ("otp","created_otp")

admin.site.register(OTP, OTPAdmin)
