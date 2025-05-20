from django import forms
from .models import *

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = DoctorModel
        fields = ['hospital', 'department']
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control py-2', 'id': 'id_hospital'}),
            'department': forms.Select(attrs={'class': 'form-control py-2', 'id': 'id_department'}),
        }
class SlotCreationForm(forms.ModelForm):
    class Meta:
        model = AppointmentSlot
        fields = ['date', 'time', 'slot_number']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control py-2', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control py-2', 'type': 'time'}),
            'slot_number': forms.NumberInput(attrs={'class': 'form-control py-2'}),
        }