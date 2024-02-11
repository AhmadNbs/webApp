from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from . import forms
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail # this library is important for the contact function
from django.template.loader import render_to_string
from django.conf import settings
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from datetime import datetime, timedelta, date
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
# Create your views here.
from django.views.decorators.http import require_http_methods
import json

def homepage(request):
    return render(request, 'appointment/homepage.html')

def appointment(request):
    # appointment_list = models.Appointment.objects.first()
    if request.method == 'POST':
        # Handle form submission
        form = forms.AppointmentForm(request.POST)
        # form = forms.AppointmentForm(request.POST, instance=appointment_list)
        if form.is_valid():
            # Check if the selected time is available
            selected_time = form.cleaned_data['appointment_time']
            selected_time = request.POST.get('appointment_time')

            date_string = selected_time

            selected_time = datetime.strptime(date_string, "%H:%M")
            ora_programare = selected_time.time().strftime("%H:%M")

            available_time_object = models.AvailableTime.objects.filter(time=selected_time).first()
            data_programare = form.cleaned_data['appointment_date'].strftime("%d/%m/%Y")
            varsta = request.POST.get('age')
            sender = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            print(str(sender))
            toemail = "ahmadshaghouri97@gmail.com"
            toname = "Alhamo Clinic"
            fromemail = form.cleaned_data['email']
            subject = "Progrmare " + str(sender)
            message = "Doamnei " + str(sender) +" "+ str(last_name) + " la varsta de " + str(varsta) + " ani, se cere o programare la ora " + str(ora_programare) + " pe data de " + str(data_programare) + "\n. Contact: " + str(fromemail)
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = subject
            html_content = message
            sender = {"name": sender, "email": fromemail}
            to = [{"email": toemail, "name": toname}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers,html_content=html_content, sender=sender, subject=subject)

            if available_time_object:
                # Save the appointment to the database with the correct appointment_time
                print(request)
                appointment = form.save(commit=False)
                appointment.appointment_time = available_time_object
                appointment.save()
                
                try:
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    pprint(api_response)
                
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
                return render(request, 'appointment/success_page.html')
            else:
                messages.error(request, 'Selected time is not available.')
    else:
        # Display the appointment form
        form = forms.AppointmentForm()
    print(request)
    return render(request, 'appointment/appointment.html', {'form': form})
    
@login_required(login_url='/admin/login/')  # Redirect to the admin login page if not authenticated
def manage_page(request):
    # Logic to fetch and display details of a specific appointment
    return render(request, 'manage.html')

def about(request):
    return render(request, 'appointment/about.html')

def services(request):
    return render(request, 'appointment/services.html')


def contact(request):
    form = forms.ContactForm
    form_submitted = False  # Initialize the variable
    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['name']
            toemail = "ahmadshaghouri97@gmail.com"
            toname = "Clinic"
            fromemail = request.POST.get('email')
            subject = "Message From" + sender
            message = request.POST.get('message_content')
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = subject
            html_content = message
            sender = {"name": sender, "email": fromemail}
            to = [{"email": toemail, "name": toname}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers,html_content=html_content, sender=sender, subject=subject)
            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
                messages.success(request, "Email send successfully")
                form_submitted = True  # Set the variable to True on successful submission
            except ApiException as e:
                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    return render(request, 'appointment/contact.html', {'form':form, 'form_submitted': form_submitted})


def appointment_list_doctor(request):
    appointments = models.Appointment.objects.all()
    return render(request, 'appointment/appointment_list_doctor.html', {'appointments': appointments})

def success_page(request):
    success_message = request.GET.get('success_message', '')
    return render(request, 'appointment/success_page.html', {'success_message': success_message})



@login_required(login_url='/admin/login/')  # Redirect to the admin login page if not authenticated
def manage_working_schedule(request):
    working_schedule = models.WorkingSchedule.objects.first() # models.Appointment.objects.first()
    if request.method == 'POST':
        form = forms.WorkingScheduleForm(request.POST, instance=working_schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Working schedule updated successfully!')
            
            update_appointment_times(working_schedule) # Update available appointment times

            return redirect('manage_working_schedule')
    else:
        form = forms.WorkingScheduleForm(instance=working_schedule)

    return render(request, 'appointment/manage_working_schedule.html', {'form': form})

@login_required(login_url='/admin/login/')  # Redirect to the admin login page if not authenticated
def manage_unavailable_dates(request):
    unavailable_dates = models.UnavailableDate.objects.all()
    if request.method == 'POST':
        form = forms.UnavailableDateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unavailable date added successfully!')
            return redirect('manage_unavailable_dates')
    else:
        form = forms.UnavailableDateForm()

    return render(request, 'appointment/manage_unavailable_dates.html', {'form': form, 'unavailable_dates': unavailable_dates})


def update_appointment_times(working_schedule):
    # Update available appointment times based on doctor's settings
    start_time = datetime.combine(datetime.today(), working_schedule.start_time)
    end_time = datetime.combine(datetime.today(), working_schedule.end_time)
    interval = working_schedule.interval

    # Calculate available times
    available_times = []
    current_time = start_time
    while current_time < end_time:
        available_times.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=interval)

    backup_data = list(models.Appointment.objects.all())
    models.AvailableTime.objects.all().delete()  # Clear existing data
    for item in backup_data:
        models.Appointment.objects.create(**item)
    for time in available_times:
        models.AvailableTime.objects.create(time=time)
        

    
# @require_http_methods(["GET"])
def clinic_appointment_list(request):
    selected_date_str = request.GET.get('appointment_date', None)

    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, '%d/%m/%Y').date()
        appointments = models.Appointment.objects.filter(appointment_date=selected_date)
    else:
        appointments = models.Appointment.objects.all()

    context = {
        'appointments': appointments,
        'selected_date_str': selected_date_str,
    }

    print(appointments)

    return render(request, 'appointment/appointment_list.html', context)


@require_http_methods(["PUT"])
def update_clinic_appointment_list(request):
    data = json.loads(request.body)
    appointment_id = data.get('appointment_id')
    status = data.get('status')
    print(status)
    print(appointment_id)


    has_updated = False
    if appointment_id:
        try:
            appointment = models.Appointment.objects.get(id=appointment_id)
            print(appointment.appointment_time)
            appointment.status = status
            
            ora_programare = appointment.appointment_time
            data_programare = appointment.appointment_date
            sender = "Alhamo Clinic"
            first_name = appointment.first_name
            toemail = appointment.email
            toname = first_name
            fromemail = "info@alhamoclinic.com"
            subject = "Progrmare " + str(toname)
            if status == "accepted":
                message = "Doamnei " + str(toname) +" "+ "cererea dumneavoastra de o programare la ora " + str(ora_programare) + " pe data de " + str(data_programare) +" a fost acceptata cu succes" + "\n. va asteptam pe Str. Viilor 52b, Cluj-Napoca 400347, Romania." +"\n. Contact: " + str(fromemail)
            else:
                message = "Doamnei " + str(toname) +" "+ "ne pare rau cererea dumneavoastra de o programare la ora " + str(ora_programare) + " pe data de " + str(data_programare) +" nu a fost acceptata din cauze anumite motive" + "\n. Va rog frumos incercati sa va programati pe alta data, sau puteti sa ne contactati pe numarul atast. Va dorim o zi buna in continuare" +"\n. Contact: " + str(fromemail)
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = subject
            html_content = message
            sender = {"name": sender, "email": fromemail}
            to = [{"email": toemail, "name": toname}]
            headers = {"Some-Custom-Name": "unique-id-1234"}
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers,html_content=html_content, sender=sender, subject=subject)
            try:
                api_response = api_instance.send_transac_email(send_smtp_email)
                pprint(api_response)
                messages.success(request, "Email send successfully")
            except ApiException as e:
                print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
            appointment.save()
            has_updated = True

        except models.Appointment.DoesNotExist:
            has_updated = False

    return JsonResponse({'updated': has_updated})

