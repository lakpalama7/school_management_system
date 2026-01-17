from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentFormModel
from django.contrib import messages
from school.forms import SchoolForms
from django.urls import reverse_lazy

# Create your views here.
@login_required
def home(request):
    try:
         request.user.school
    except Exception as e:
         print(e)
         #messages to welcome school admin and direct them to school register
         message={
              "Welcome to the dashboard ! Please register your school to get started"
         }
         messages.info(request,message)

         school_reg_form = SchoolForms()
         form_submission_url = reverse_lazy('school:school_register')
         context = {
              "form" : school_reg_form,
              "form_submission_url": form_submission_url,
         }
         return render(request,"main/dashboard.html", context)

    stat=[
        {
           'title':'Total Student',
           'data':1230,
           'text_color':'text-primary' 
        },
        {
           'title':'Total Payment',
           'data':'Rs. 450000',
           'text_color':'text-green-600' 
        },
        {
           'title':'Pending Payment',
           'data':'Rs. 12000',
           'text_color':'text-red-600' 
        },
        {
           'title':'Active Classes',
           'data':32,
           'text_color':'text-secondary' 
        },

    ]
    context={
        'stat':stat
    }
    return render(request, 'main/dashboard.html',context)


def student_register(request):
    
        if request.method == 'POST':
            form=StudentFormModel(request.POST)
            print("-----",request.POST)
            if not form.is_valid():
                print("-----------", form.errors)
                context={
                    'form_new':form
                }
            
                return render(request,'main/student_register.html',context)
            form.save()

            return redirect('student_register')
        
        form = StudentFormModel()
        context={
                 'form_new':form
            }
        return render(request,'main/student_register.html', context)

# def student_register(request):

#     if request.method == 'POST':
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         address=request.POST['address']
#         phone=request.POST['phone']

#         errors={}
#         if not len(phone) == 10:
#             errors['phone']="Phone number must be 10 digits"

#         if len(errors.keys())>0:
#             form_data={ 
#                 'first_name':first_name,
#                 'last_name':last_name,
#                 'address':address,
#                 'phone':phone,
#             }
#             context={
#                 'errors':errors,
#                 'form_data':form_data,
#             }
#             return render(request, 'main/student_register.html', context)
        
#         return redirect('home')
    
#     return render(request,'main/student_register.html')


