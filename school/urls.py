from django.urls import path
from school import views

app_name = "school"
urlpatterns = [
    path("register/", views.school_register, name="school_register"),
    path("profile/",views.school_profile, name="school_profile"),
    path("update/",views.update_school, name="update_school"),
    path("grade/", views.grade, name="grade"),
]
