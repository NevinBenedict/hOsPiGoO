from django.urls import path
from .views import *

urlpatterns = [

    path('slotlist/<int:pk>', SlotListView.as_view(), name='slotlist'),
    path('appointment/<int:pk>', AppointmentBookingView.as_view(), name='appointment'),
    path('patienthome/', PatientHomeView.as_view(), name='patienthome'),
    path('department/<int:pk>', DepartmentView.as_view(), name='department'),
    path('doctorlist/', DoctorList.as_view(), name='doctorlist'),
    path('patientapp/',AppointmentPatientDisplayView.as_view(),name='patientappdis'),
    path('slotdisplay/<int:pk>', SlotDisplayView.as_view(), name='slotdisplays'),
    
    
]