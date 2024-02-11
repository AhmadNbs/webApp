from django.contrib import admin
from .models import Appointment, RomaninHolidays, WorkingSchedule, UnavailableDate, AvailableTime
# Register your models here.


admin.site.site_header = 'Alhamo Clinic Adminstration'
admin.site.site_title = 'Alhamo Site Adminstration'

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'age', 'email', 'appointment_date', 'appointment_time', 'status']
    list_display_links = ['last_name', 'first_name', 'email']
    list_editable = ['appointment_date', 'appointment_time', 'status']
    search_fields = ['first_name','last_name']
    list_filter = ['appointment_date']

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(RomaninHolidays)
admin.site.register(WorkingSchedule)
admin.site.register(UnavailableDate)
admin.site.register(AvailableTime)

