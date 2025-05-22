from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout 
from .models import *
from userapp.models import CustomUser
from .forms import *
from datetime import  timedelta,datetime,date
from django.http import JsonResponse
from bookingapp.models import *

# Create your views here.

class DoctorHomeView(View):
    def get(self, request):
        appointmentslot=AppointmentSlot.objects.filter(doctor=request.user)
        min_date = (date.today() + timedelta(days=1)).isoformat()
        max_date = (date.today() + timedelta(days=7)).isoformat()
        user= CustomUser.objects.get(id=request.user.id)
        doctor = DoctorModel.objects.get(doctor=user)
        patient = AppointmentBooking.objects.filter(doctor=user,status="Success")

        patients_con= AppointmentBooking.objects.filter(doctor=user,status="Success").count()
       
        m_date = date.today() - timedelta(days=30)
        p_count = AppointmentBooking.objects.filter(doctor=user,status="Success", appointment_date__gte=m_date).count()

        
        return render(request, 'doctorhome.html',{'appointmentslot': appointmentslot, 'min_date': min_date , 'max_date': max_date,'doctor': doctor,'patient':patient,'patients_con': patients_con ,'p_count':p_count})


def get_departments(request):
    hospital_id = request.GET.get('hospital_id')
    departments = DepartmentModel.objects.filter(hospital_id=hospital_id).values('id', 'name')
    return JsonResponse(list(departments), safe=False)  

class DoctorRegistrationView(View):
    def get(self, request):
        form= DoctorRegistrationForm()
        print(request.session['user'])
        return render(request, 'doctorregistration.html', {'form': form})

    def post(self, request):
        form= DoctorRegistrationForm(request.POST)
       
        if form.is_valid():
            print(request.session['user'])
            hospital = form.cleaned_data['hospital']
            department = form.cleaned_data['department']
            user= CustomUser.objects.get(id=request.session['user'])
            doctor = DoctorModel.objects.create(doctor=user,hospital=hospital, department=department)
            return redirect('login')
        return render(request, 'doctorregistration.html', {'form': form})

class SlotCreationView(View):
    # def get(self, request):
    #     form= SlotCreationForm()
    #     return render(request, 'slotcreation.html', {'form': form})
    def post(self, request):
        # form= SlotCreationForm(request.POST)
        
            doctor = CustomUser.objects.get(id=request.user.id)
            date = request.POST['date']
            time = request.POST['time']
            slot_number = int(request.POST['slot_number'])

            date = datetime.strptime(date, "%Y-%m-%d").date()
            time = datetime.strptime(time, "%H:%M").time()

            is_slot_exists = AppointmentSlot.objects.filter(doctor=doctor, date=date).exists()
            if is_slot_exists:
                appointmentslot = AppointmentSlot.objects.filter(doctor=doctor)
                min_date = (date.today() + timedelta(days=1)).isoformat()
                max_date = (date.today() + timedelta(days=7)).isoformat()
                return render(request, 'doctorhome.html', {
                'appointmentslot': appointmentslot,
                'min_date': min_date,
                'max_date': max_date,
                'slot_exists_popup': True
            })


            Slot = AppointmentSlot.objects.create(doctor=doctor, date=date, time=time, slot_number=slot_number)
            current_time = datetime.combine(date, time)  # Combine to datetime object
            for i in range(slot_number):
                Slotdivide.objects.create(
                    slot=Slot,
                    slot_name=i+1,
                    date=date,
                    time=current_time.time()  # Save only the time part if needed
                )
                current_time += timedelta(minutes=15)
            return redirect('doctorhome')
     
    
class SlotDisplayView(View):
    def get(self, request,pk):
        
        doctor = CustomUser.objects.get(id=request.user.id)
        slots = Slotdivide.objects.filter(slot=pk,slot__doctor=doctor)
        min_date = (date.today() + timedelta(days=1)).isoformat()
        max_date = (date.today() + timedelta(days=7)).isoformat()
        return render(request, 'slotdisplay.html', {'slots': slots,'min_date':min_date,"max_date":max_date})

class SlotDelete(View):
    def post(self, request, pk):
        slot = AppointmentSlot.objects.get(id=pk,doctor=request.user)
        appointment=AppointmentBooking.objects.filter(slot__slot=slot)
        for i in appointment:
            print(i.status)
            i.status="Cancelled by Doctor"
            i.save()
            print(i.status)
        slot.delete()
        return redirect('doctorhome')

class AppointmentDoctorDisplay(View):
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        print(user)
        min_date = (date.today() + timedelta(days=1)).isoformat()
        max_date = (date.today() + timedelta(days=7)).isoformat()
        appointment = AppointmentBooking.objects.filter(doctor=user,pay_status="Success")
        for i in appointment:
            if (i.appointment_date+timedelta(days=2)<date.today()) and (i.status=="pending"):

                i.status="Cancelled"
                i.save()
        return render(request, 'appointmentdoctor.html', {'appointments': appointment,'min_date':min_date,'max_date':max_date})

class AppointmentDetailDisplay(View):
    def get(self, request, pk):
        slot = Slotdivide.objects.get(id=pk)
        
        appointment = AppointmentBooking.objects.get(slot=slot.id)
        min_date = (date.today() + timedelta(days=1)).isoformat()
        max_date = (date.today() + timedelta(days=7)).isoformat()
        
        return render(request, 'appointmentdetai.html', {'appointment': appointment,'min_date':min_date,"max_date":max_date})

class Appointmentstatus(View):
    def get(self, request, pk):
        today = date.today()
        appointment = AppointmentBooking.objects.get(id=pk)
        if appointment.appointment_date <= today and appointment.status == "Pending":
            appointment.status = "Success"
            appointment.save()
        elif appointment.status=="Success":
            appointment.status = "Pending"
            appointment.save()

        return redirect('appdoctor')

class HospitalDetailView(View):
    def get(self,request,pk):
        hospital=HospitalModel.objects.get(id=pk)
        dept=DepartmentModel.objects.filter(hospital=hospital)
        doctor=DoctorModel.objects.filter(hospital=hospital)
        return render(request,"hospitaldetail.html",{'hospital':hospital,'dept':dept,'doctor':doctor})