from .models import Student
from django import forms
class StudentFormModel(forms.ModelForm):
    
    class Meta:
        model=Student
        fields="__all__"
        #fields = ['first_name','last_name','address','email','phone']

        widgets = {
            "first_name":forms.TextInput(attrs={"class":"input w-full"}),
            "last_name":forms.TextInput(attrs={"class":"input w-full"}),
            "address":forms.TextInput(attrs={"class":"input w-full"}),
            "email":forms.EmailInput(attrs={"class":"input w-full"}),
            "phone":forms.TextInput(attrs={"class":"input w-full"}),
        } 

    def clean_phone(self):
        phone=self.cleaned_data['phone']

        try:
            int(phone)
        except ValueError:
            raise forms.ValidationError("Phone number must be numeric")
        
        if phone[:2] not in ['98','97']:
            raise forms.ValidationError("Phone number must start with 98 or 97 only...")
        
        if not len(phone) == 10:
            raise forms.ValidationError("Phone number must be 10 digits.")
        
        return phone


