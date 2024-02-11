# In your forms.py file in the 'appointment' app

from django import forms
from . import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, time, date
# from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
class WorkingScheduleForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
        label='Start Time'
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
        label='End Time'
    )

    interval = forms.ChoiceField(
        choices=[(str(i), str(i) + ' mins') for i in range(1, 61)],
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    class Meta:
        model = models.WorkingSchedule
        fields = ['start_time', 'end_time', 'interval']

class UnavailableDateForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
        label='Select Unavailable Date'
    )
    class Meta:
        model = models.UnavailableDate
        fields = [ 'date', 'reason']



# Appointment App 


class AppointmentForm(forms.ModelForm):
        
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter your age', 'size': 3, 'maxlength': 3, 'class': 'form-input'})
    )

    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 1:
            raise forms.ValidationError("Age must be a positive integer.")
        return age

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'size': 30, 'maxlength': 50, 'class': 'form-input'})
    )
    
    current_date = timezone.now().date()
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'Select appointment date', 'size': 10, 'class': 'form-input', 'type': 'date', 'min': current_date.isoformat()}),
        #validators=[validate_date_today_or_later]  # Example: Date must be today or later
    )


    available_times = models.AvailableTime.objects.values_list('time', flat=True)
    choices = [(time.strftime('%H:%M'), time.strftime('%H:%M')) for time in available_times]
    appointment_time = forms.ChoiceField(
    choices=choices,
    widget=forms.Select(attrs={'class': 'form-input'}),
    )



    class Meta:
        model = models.Appointment
        fields = ['first_name', 'last_name', 'age', 'email', 'appointment_date', 'appointment_time']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'size': 30, 'maxlength': 30, 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'size': 30, 'maxlength': 30, 'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('appointment_date')
        appointment_time_str = cleaned_data.get('appointment_time')
        
        # Convert the string time to a datetime.time object
        try:
            appointment_time = datetime.strptime(appointment_time_str, '%H:%M').time()
        except ValueError:
            raise forms.ValidationError('Invalid time format. Please select a valid time.')

        if appointment_date < timezone.now().date():
            raise forms.ValidationError('Appointment date must be in the future.')

        # Check if the selected time is in the future
        if appointment_date == timezone.now().date() and appointment_time <= timezone.now().time():
            raise forms.ValidationError('Appointment time must be in the future.')

        # Fetch the AvailableTime instance based on the selected time
        available_time_instance = models.AvailableTime.objects.filter(time=appointment_time).first()

        if not available_time_instance:
            raise forms.ValidationError('Selected time is not available.')

        # Assign the AvailableTime instance to the appointment_time field
        cleaned_data['appointment_time'] = available_time_instance

        return cleaned_data
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your email', 'size': 30, 'maxlength': 50, 'class': 'form-input'})
    )
    message_content = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'your message'}))

