from .background_task import send_otp
def is_email_valid(email):
    if email is not None and email!=" " and "@"  in email and "."  in email:
        return True
    return False


     
def forget_password_email(email):
        from . models import OTP

        try:
             new_otp=OTP.generate_otp(email) 
        except Exception as e:
             raise Exception(str(e))
        send_otp(email,new_otp)
        
        