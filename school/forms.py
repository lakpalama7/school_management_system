from django import forms
from school.models import School, Grade
from django.utils.text import slugify 

class SchoolForms(forms.ModelForm):
    class Meta:
        model = School
        exclude = (
            'admin_user',
            'created_at',
            'slug',
            'code',
            'updated_at',
            'is_active',
        )

        widgets = {
            "established_date": forms.DateInput(attrs={"type":"date"}),
            "theme_color":forms.TextInput(attrs={"type":"color"}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)
    def save(self, commit = True, *args, **kwargs ):
        school = super(SchoolForms, self).save(commit=False, *args, **kwargs)
        
        if self.request:
            school.admin_user = self.request.user
        
        if not school.code:
            # school.admin_user = request.user
            # print("Admin user: ", request.user)

            school_year = self.cleaned_data.get("established_date").year
            school_name = self.cleaned_data.get('name')
            school_code_name = school_name.split(" ")
            school_code = "".join([name[0] for name in school_code_name]) + f"-{school_year}"

            school.code = school_code
            school.slug = slugify(school_name)

        if commit:
            school.save()
        return school
    

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") if "request" in kwargs else None
        super().__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        grade = super(GradeForm, self).save(commit=False, *args, **kwargs)
        grade.school = self.request.user.school

        if commit:
            grade.save()
        return grade