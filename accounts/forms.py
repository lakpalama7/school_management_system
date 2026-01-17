from django import forms
from .models import CustomUser



class SchoolAdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'input ','placeholder':'Enter username'}),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'input','placeholder':'Enter password'}),
    )
class SchoolAdminRegisterForm(forms.Form):
    username = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class':'input w-full', 'placeholder':'Enter your name'}),
                               )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'input w-full','placeholder':'Enter your email'}),
                             )
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input w-full','placeholder':'Enter your password'}),
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input w-full','placeholder':'Re-enter your password'}),
                                )

    first_name = forms.CharField(max_length=50,
                                 widget=forms.TextInput(attrs={'class':'input w-full','placeholder':'Enter your first name'}),
                                 )
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'input w-full','placeholder':'Enter your last name'}),
                                )
    phone_number = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class':'input w-full','placeholder':'Enter phone no'}),
                            )
    address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class':'input w-full','placeholder':'Enter your address '}),
                              )
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "file-input w-full p-2"}),)
    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Password do not match")
    def save(self, commit=True):
        user = CustomUser(
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            phone_number = self.cleaned_data['phone_number'],
            address = self.cleaned_data['address'],
            profile_pic = self.cleaned_data['profile_pic'],
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

