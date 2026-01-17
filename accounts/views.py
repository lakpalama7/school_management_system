from django.shortcuts import render,redirect
from .forms import SchoolAdminRegisterForm,SchoolAdminLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . models import OTP, CustomUser
from django.contrib.auth.password_validation import validate_password

from . import utils
# Create your views here.
def school_admin_register(request):

    if request.method == 'POST':
        form = SchoolAdminRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("accounts:school_admin_login")
        context={
            'forms':form
        }
        return render(request,'accounts/register.html',context)

    forms=SchoolAdminRegisterForm()
    context={
        'forms':forms
    }
    return render(request,'accounts/register.html',context)


def school_admin_login(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("main:home")
        messages.error(request, "Invalid username or password")
        return redirect("accounts:school_admin_login")
        
    forms = SchoolAdminLoginForm()
    context={
        'forms':forms
    }
    return render(request,'accounts/login.html',context)

def logout_view(request):
    logout(request)
    return redirect("accounts:school_admin_login")

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print(utils.is_email_valid(email),"-------------------------------")
        if not utils.is_email_valid(email):
            messages.error(request, "Email is required")
            return redirect("accounts:forgot_password")
        try:
            utils.forget_password_email(email)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("accounts:forgot_password")
        
        messages.success(request, "Email send successfully. Please check your inbox")
        return redirect("accounts:otp_confirmation")
    
    return render(request,'accounts/forgot_password.html')

def opt_confirmation(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        print("OTP-----", otp)

        user_id = OTP.check_otp(otp)
        if user_id is None:
            messages.error(request, "Your OTP is expired")
            return redirect("accounts:otp_confirmation")
        
        return redirect('accounts:set_new_password', user_id=user_id)
        
    return render(request,'accounts/otp_confirmation.html')

def set_new_password(request, user_id):

    if request.method == 'POST':
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Password do not match")
            return redirect('accounts:set_new_password',user_id=user_id)
        try:
            validate_password(password1)
        except Exception as e:
            for error in list(e):
                messages.error(request, str(error))
                return redirect('accounts:set_new_password',user_id=user_id)
        else:
            if user_id is not None:
                user = CustomUser.objects.filter(id=user_id).first()

                if user is None:
                    messages.error(request, "User does not exists")
                    return redirect('accounts:set_new_password',user_id=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('accounts:school_admin_login')
    return render(request, 'accounts/newpassword.html')