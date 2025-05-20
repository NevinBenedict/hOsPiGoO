from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('docreg', DoctorRegistrationView.as_view(), name='docreg'),
    path('slotcreation', SlotCreationView.as_view(), name='slotcreation'),
    path('slotdisplay/<int:pk>', SlotDisplayView.as_view(), name='slotdisplay'),
    path('slotdelete/<int:pk>/', SlotDelete.as_view(), name='slotdelete'),
    path('doctorhome', DoctorHomeView.as_view(), name='doctorhome'),
    path('ajax/get-departments/', get_departments, name='get_departments'),
    path('appdoctor/', AppointmentDoctorDisplay.as_view(), name='appdoctor'),
    path('appdetail/<int:pk>', AppointmentDetailDisplay.as_view(), name='appdetail'),
    path('appstatus/<int:pk>',Appointmentstatus.as_view(),name="appstatus"),
    path('hosdetails/<int:pk>',HospitalDetailView.as_view(),name="hosdetails"),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)