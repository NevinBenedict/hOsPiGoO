from django.contrib import admin
from .models import *
from userapp.models import CustomUser


# Register your models here.
admin.site.register(HospitalModel)
admin.site.register(DoctorModel)
admin.site.register(CustomUser)
admin.site.register(DepartmentModel)