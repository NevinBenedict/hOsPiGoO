from django.shortcuts import render,redirect
from django.views.generic import View
from django.utils import timezone
from hospitalapp.models import *
from userapp.models import CustomUser
from .models import *
from .forms import *    
from django.contrib import messages
from datetime import datetime, timedelta,date

# Create your views here.
class SlotListView(View):
    def get(self, request,pk):
        slots = Slotdivide.objects.filter(slot=pk)
        return render(request, 'slotlist.html', {'slots': slots})

class BookingSystem():
    def get(self,request):
        hospital= HospitalModel.objects.all()
        department=HospitalModel.objects.all()
        return render(request,"appsystem.html",{'hospital':hospital,'department':department})
    
     
    
class AppointmentBookingView(View):
    
    def post(self,request,pk):
        slot=Slotdivide.objects.get(id=pk)
        app=AppointmentSlot.objects.get(id=slot.slot.id)
        doctor = CustomUser.objects.get(id=slot.slot.doctor.id)
        patient = CustomUser.objects.get(id=request.user.id)
        date = slot.date
        time=slot.time

        # Check if the slot is already booked'
        Appointment = AppointmentBooking.objects.filter(slot__slot=app).exists()
        if Appointment:
            message=messages.error(request, "You have already booked a slot . ")
            print(slot.slot.doctor.docrelate)
            return redirect('slotdisplays', pk=slot.slot.doctor.docrelate.id,)
        
        
        appointment = AppointmentBooking.objects.create(doctor=doctor, patient=patient, slot=slot,status='Pending',appointment_date=date,appointment_time=time)
        appointment.save()
        slot.is_booked = True
        slot.save()
        
        return redirect('slotdisplays', pk=slot.slot.doctor.docrelate.id)

    
class PatientHomeView(View):
    def get(self, request):
        data=HospitalModel.objects.all()
        departments=DepartmentModel.objects.all()
        return render(request, 'patienthome.html',{'data':data,'departments':departments})

class DepartmentView(View):
    def get(self,request,pk):
        hos=HospitalModel.objects.get(id=pk)
        data=DepartmentModel.objects.filter(hospital=hos)
        return render(request, 'department.html',{'data':data})
class DoctorList(View):
    def post(self,request):
        hospital=HospitalModel.objects.get(id=request.POST["hospital"])
        data=DoctorModel.objects.filter(hospital=hospital,department=request.POST["department"])
        print(data)
        return render(request, 'doctorlist.html',{'doctors':data})

class SlotDisplayView(View):
    def get(self, request, pk):
        doc = DoctorModel.objects.get(id=pk)
        doctor = CustomUser.objects.get(id=doc.doctor.id)
        date_str = request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                slot = Slotdivide.objects.filter(slot__doctor=doctor, date=date_obj)
            except ValueError:
                # Handle invalid date format gracefully
                slot = Slotdivide.objects.none()
        else:
            tomorrow = timezone.now().date() + timedelta(days=1)
            all_dates = Slotdivide.objects.filter(slot__doctor=doctor).values_list('date', flat=True).distinct().order_by('date')
            slot = Slotdivide.objects.filter(slot__doctor=doctor, date=all_dates[0])        # Get all unique dates for this doctor for the date picker
        all_dates = Slotdivide.objects.filter(slot__doctor=doctor).values_list('date', flat=True).distinct().order_by('date')
        return render(request, 'slotlist.html', {'slots': slot, 'all_dates': all_dates, 'selected_date': date_str})


class AppointmentPatientDisplayView(View):
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        appointment = AppointmentBooking.objects.filter(patient=user)
        return render(request, 'appointment.html', {'appointments': appointment})



