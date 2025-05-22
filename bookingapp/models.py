from django.db import models
from userapp.models import CustomUser
from hospitalapp.models import *

# Create your models here.

class AppointmentBooking(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='doctor_booking')
    patient=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_booking')
    slot = models.ForeignKey(Slotdivide, on_delete=models.SET_NULL, null=True, blank=True, related_name='slot_num')
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Cancelled', 'Cancelled'),
    ])
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True)
    pay_status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.username} "

class PaymentModel(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    order_id=models.CharField(max_length=100)

    payment_status=models.BooleanField(default=False)

    payment_id=models.CharField(max_length=100,null=True,blank=True)

    total=models.FloatField()

    date=models.DateField(auto_now_add=True)