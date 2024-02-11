#import holidays
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class RomaninHolidays(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)
    
class WorkingSchedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(60)],
        help_text="Enter the interval between appointments in minutes."
    )

    def __str__(self):
        formatted_start_time = self.start_time.strftime('%H:%M')  # Format hours in 24-hour clock
        formatted_end_time = self.end_time.strftime('%H:%M')
        return f"{formatted_start_time} - {formatted_end_time} - {self.interval} minutes"


class UnavailableDate(models.Model):
    date = models.DateField()
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.reason}"
    
    
class AvailableTime(models.Model):
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime('%H:%M')


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('', '---------'),
        ('accepted', 'Accept'),
        ('refused', 'Refuse'),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField()
    email = models.EmailField(blank=True, null=True, max_length=50)
    appointment_date = models.DateField()
    appointment_time = models.ForeignKey(AvailableTime, on_delete=models.CASCADE, null=True, blank=True, default=None)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['appointment_date', 'appointment_time'], name='date_time_uk')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date} {self.appointment_time}"