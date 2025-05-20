from django.db import models
from userapp.models import CustomUser
from django.contrib.auth.hashers import make_password

# Create your models here.
class HospitalModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password= models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    address=models.CharField(max_length=100,null=True)
    description =models.TextField(max_length=500,null=True)
    image = models.ImageField(upload_to='hospital/',null=True,blank=True)

    def save(self, *args, **kwargs):
        # Only hash if not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DepartmentModel(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(HospitalModel, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    
    
class DoctorModel(models.Model):
   

    doctor= models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='docrelate')
    hospital = models.ForeignKey(HospitalModel, on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor.username} - {self.department.name} ({self.hospital.name})"

class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    slot_number = models.PositiveIntegerField(default=5)
    

class Slotdivide(models.Model):
    
    slot_name = models.PositiveIntegerField()
    slot = models.ForeignKey(AppointmentSlot, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)
    date= models.DateField()
    time= models.TimeField()

