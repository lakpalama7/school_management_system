from background_task import background

@background(schedule=3)
def send_otp(email,new_otp):  #background task
    from django.core.mail import send_mail
    from django.conf import settings
    subject = "password reset"
    message = f""" 
        use the following OTP to reset your password: {new_otp}
        OR
        follow the link to go to the OTP confirmation page: http://127.0.0.1:8000/accounts/forgot-password/
        """
        
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
