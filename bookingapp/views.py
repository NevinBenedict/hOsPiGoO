from django.shortcuts import render,redirect
from django.views.generic import View
from django.utils import timezone
from hospitalapp.models import *
from userapp.models import CustomUser
from .models import *
from .forms import *    
from django.contrib import messages
from datetime import datetime, timedelta,date
import razorpay

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
        
        
        appointment = AppointmentBooking.objects.create(doctor=doctor, patient=patient, slot=slot,status='Pending',appointment_date=date,appointment_time=time,pay_status='Pending')
        appointment.save()
        slot.is_booked = True
        slot.save()
        
        return redirect('payintiate', pk=appointment.id)

    
class PatientHomeView(View):
    def get(self, request):
        appointment=AppointmentBooking.objects.filter(patient=request.user.id,pay_status="Cancelled")
        if appointment:
            for i in appointment:
            
                slot=Slotdivide.objects.get(id=i.slot.id)
                slot.is_booked=False
                slot.save()
            appointment.delete()

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
        appointment = AppointmentBooking.objects.filter(patient=user,pay_status="Success")
        return render(request, 'appointment.html', {'appointments': appointment})


class PaymentIntiate(View):
    def get(self,request,pk):

        user=CustomUser.objects.get(id=request.user.id)
        appointment=AppointmentBooking.objects.get(id=pk)

        client = razorpay.Client(auth=("rzp_test_geSQxmqjudttbo", "vl4T8QIcv8pU8o7UF6vZAIVw"))

        DATA = {
            "amount": 500*100,
            "currency": "INR",
    
                }
        
        data = client.order.create(data=DATA)
        order_id = data['id']
        summary = PaymentModel.objects.create(user=user,order_id=order_id,total=500)
        context={'summary':summary,'Appointment':appointment,'razorpaykey_id':"rzp_test_geSQxmqjudttbo",'order_id':order_id,'amount':data['amount'],'user':user}
        appointment.pay_status="Cancelled"
        appointment.save()
        return render(request,"payment.html",context)
    
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')       
class PaymentSuccess(View):
    def post(self, request):
            # Log Razorpay's callback data
            print(request.POST)

            # Extract data from the callback
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Verify Razorpay signature
            client = razorpay.Client(auth=("rzp_test_geSQxmqjudttbo", "vl4T8QIcv8pU8o7UF6vZAIVw"))
            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
            except razorpay.errors.SignatureVerificationError:
                print("Payment verification failed.")
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect('patienthome')

            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                print("User is not authenticated.")
                
                order_items = AppointmentBooking.objects.filter(patient=user, status="pending")
                for i in order_items:
                    i.pay_status="Cancelled"
                    i.save()
                messages.error(request, "Something went wrong. Order Cancelled")
                return redirect('patienthome')

            # Fetch the user
            
            
            user = CustomUser.objects.get(id=request.user.id)

            # Update payment status in the database
            summary = PaymentModel.objects.filter(user=user, payment_status=False)
            for i in summary:
                i.payment_status = True
                i.payment_id = razorpay_payment_id
                i.save()

            # Update stock and order item status
            
            order_items = AppointmentBooking.objects.filter(patient=user, status="pending")
            for i in order_items:
                i.pay_status = "Success"
                i.save()

            messages.success(request, "Payment successful! Your order has been placed.")
            return redirect('patienthome')

       