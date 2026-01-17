from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from school.forms import SchoolForms, GradeForm
from school.models import School
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import IntegrityError
# Create your views here.
@require_POST
def school_register(request):
    form_data = request.POST
    form = SchoolForms(form_data, request.FILES, request=request)

    if form.is_valid():
        form.save()
        return redirect("school:school_profile")
    
    return render(request, "main/dashboard.html", {"form":form})

@require_GET
@login_required
def school_profile(request):
    school_admin = request.user
    try:
        school_data = school_admin.school
    except Exception as e:
        print(e)
        return redirect("main/home")
    context = {
        "admin":school_admin,
        "school": school_data
    }
    return render(request, 'school/profile.html',context)


@login_required
def update_school(request):
    if request.method == 'POST':
        form_data = request.POST
        form = SchoolForms(form_data, request.FILES, instance=request.user.school, request=request)

        if form.is_valid():
            
            form.save()
            return redirect("school:school_profile")
    form = SchoolForms(instance=request.user.school, request=request)
    form_submission_url = reverse_lazy('school:update_school')
    context ={
        "form": form,
        "form_submission_url":form_submission_url,
    }
    return render(request, "school/update-school-info.html",context)


def grade(request):
    if request.method == "POST":
        form = GradeForm(request.POST, request=request)

        if form.is_valid():
            try:
                saved_grade= form.save() #return model instance
            except IntegrityError:
                return JsonResponse(
                    {"success":False,
                     "message": "Grade already exists."}
                )
            else:
                saved_grade_data ={
                    "id":saved_grade.id,
                    "name":saved_grade.name,
                }
                return JsonResponse({
                        "success": True,
                        "message":"Grade added successfully",
                        "data": saved_grade_data,
                    })
    form = GradeForm()
    grade_list = request.user.school.classes.all() #get all the grade list of current user school
    context = {
        "form":form,
        "grade_list":grade_list,
    }
    return render(request,"school/grade-form.html", context)

