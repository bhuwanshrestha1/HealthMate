from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from home.models import CustomUser,Doctor, DoctorAvailability,Appointment, NewReport
from .mlcode.main import predict_disease_and_specialist
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.middleware.csrf import get_token
from .forms import SymptomForm
from datetime import datetime, date, timedelta, time
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')


def patient_details(request):
    return render(request,'patient_details.html')




def patient_register(request):
    if request.method== "POST":
        username=request.POST.get('username')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username is already used.")
            return redirect('patient_register')
        

        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already used.")
            return redirect('patient_register')

        contact=request.POST.get('contact')
        if CustomUser.objects.filter(contact=contact).exists():
            messages.error(request, "Number is already used.")
            return redirect('patient_register')
        
        age=request.POST.get('age')
        sex = request.POST.get('sex')  
        address = request.POST.get('address')
        password=request.POST.get('password')

        myuser=CustomUser.objects.create_user(username,email,password)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.age= age
        myuser.contact= contact
        myuser.sex = sex
        myuser.address = address

        if 'profile_image' in request.FILES:
            myuser.profile_image = request.FILES['profile_image']

        myuser.save()

        messages.success(request,"Your account has been successfully created.")

        return redirect('patient_login')


    return render(request,'patient_register.html')

def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pass1')

        user = authenticate(username=username, password=password)

        if user is not None and not user.is_superuser:
            try:
                doctor = user.doctor  # Assuming there's a one-to-one relationship between CustomUser and Doctor
            except Doctor.DoesNotExist:
                doctor = None

            if doctor is not None:
                messages.error(request, "Invalid username or password.")
                return redirect('patient_login')
            else:
                login(request, user)
                return redirect('patient_profile')  # Redirect to the profile page after successful login

    return render(request, 'patient_login.html')



def log_out(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('patient_login')

def log_out1(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('doctor_login')

def doctor_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using CustomUser model
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if the user is a doctor
            try:
                doctor = user.doctor  # Assuming there's a one-to-one relationship between CustomUser and Doctor
            except Doctor.DoesNotExist:
                doctor = None

            if doctor is not None:
                # If the user is a doctor, log in
                login(request, user)
                print("Login Successful!")
                return redirect('doctor_home')
            else:
                print("User is not a doctor.")
                messages.error(request, "Invalid credentials for a doctor.")
                return redirect('doctor_login')
        else:
            print("Authentication failed.")
            messages.error(request, "Invalid credentials for a doctor.")
            return redirect('doctor_login')

    return render(request, 'doctor_login.html')

def book_appointment(request):
    
    return render(request,'book_appointment.html')

def doctor_home(request):
    return render(request,'doctor_home.html')

def doctor_profile(request):
    return render(request,'doctor_profile.html')

def patient_profile(request):
    return render(request,'patient_profile.html')

def admin_login(request):
    if request.method == 'POST':
        admin_user = request.POST.get('admin_user')
        admin_pass = request.POST.get('admin_pass')

        # Authenticate the user
        user = authenticate(request, username=admin_user, password=admin_pass)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin_profile')  # Change this to your admin profile URL
        else:
            messages.error(request, 'Invalid credentials for admin.')
    
    return render(request, 'admin_login.html')

def result_template(request):
    return render(request,'result_template.html')


def book_recommendation(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptom1 = form.cleaned_data['symptom1']
            symptom2 = form.cleaned_data['symptom2']
            symptom3 = form.cleaned_data['symptom3']
            symptom4 = form.cleaned_data['symptom4']

            # Check if only one symptom is provided
            selected_symptoms = [symptom for symptom in [symptom1, symptom2, symptom3, symptom4] if symptom != 'None']
            if len(selected_symptoms) < 2:
                form.add_error(None, "Please provide at least two symptoms.")
                return render(request, 'book_recommendation.html', {'form': form})

            # Call your machine learning function
            prediction_result, specialist = predict_disease_and_specialist(symptom1, symptom2, symptom3, symptom4)

            # Pass the result to the template
            return render(request, 'result_template.html', {'result': prediction_result, 'specialist': specialist})
    else:
        # Set initial values for the form fields to None
        form = SymptomForm(initial={'symptom1': None, 'symptom2': None, 'symptom3': None, 'symptom4': None})

    return render(request, 'book_recommendation.html', {'form': form})


def book_no_recommendation(request):
    all_specialities = set(Doctor.objects.values_list('specialities', flat=True))
    speciality_filter = request.GET.get('speciality')

    if speciality_filter:
        filtered_doctors = Doctor.objects.filter(specialities__iexact=speciality_filter)
    else:
        filtered_doctors = Doctor.objects.all()

    return render(request, 'book_no_recommendation.html', {
        'doctors': filtered_doctors,
        'all_specialities': all_specialities,
        'selected_speciality': speciality_filter,
    })

from django.utils import timezone

def book_now(request, doctor_id):
    if request.method == 'POST':
        # Extract form data from the POST request
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        appointment_reason = request.POST.get('appointment_reason')
        old_reports = request.FILES.get('old_reports')

        doctor = get_object_or_404(Doctor, user_id=doctor_id)
        if Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date, appointment_time=appointment_time).exists() :
            messages.error(request, "Selected time is not available. Please choose another time.")
            # Preserve the selected time and date in the session for displaying in the form
            request.session['selected_appointment_date'] = appointment_date
            request.session['selected_appointment_time'] = appointment_time
            return redirect('book_now', doctor_id=doctor_id)
    

        # Clear the session variables if booking is successful
        request.session.pop('selected_appointment_date', None)
        request.session.pop('selected_appointment_time', None)
        
        # Create an Appointment instance
        appointment = Appointment.objects.create(
            patient=request.user,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=appointment_reason,
            old_reports=old_reports,
        )

        # Update any other logic based on appointment creation, for example, setting doctor's availability status
        doctor.is_booked = True
        doctor.save()

        messages.success(request, "Appointment booked successfully.")
        return redirect('patient_profile')
    else:
        doctor = get_object_or_404(Doctor, user_id=doctor_id)
        today = date.today()
        days = [today + timedelta(days=i) for i in range(10)]  # Today and next 5 days

        available_days = [day.day.lower() for day in doctor.availability_days.all()]

        break_start1 = datetime.combine(today, doctor.break_start1)
        break_end1 = datetime.combine(today, doctor.break_end1)
        break_start2 = datetime.combine(today, doctor.break_start2)
        break_end2 = datetime.combine(today, doctor.break_end2)

        interval = timedelta(minutes=30)
        time_options = []
        current_time = datetime.combine(today, doctor.start_time)
        end_datetime = datetime.combine(today, doctor.end_time)

        while current_time < end_datetime:
            if not (break_start1 <= current_time < break_end1) and not (break_start2 <= current_time < break_end2):
                time_options.append(current_time.strftime("%H:%M"))

            current_time += interval

        available_dates = [
            {
                'day': (today + timedelta(days=i)).strftime('%A'),
                'date': (today + timedelta(days=i)).strftime("%Y-%m-%d")
            }
            for i in range(1,11) if (today + timedelta(days=i)).strftime('%A').lower() in available_days
        ]
        context = {
            'doctor': doctor,
            'time_options': time_options,
            'available_dates': available_dates,
        }

        return render(request, 'book_now.html', context)


def admin_profile(request):
    return render(request, 'admin_profile.html')

def my_appointment(request):
    # Activate the local time zone
    timezone.activate("Asia/Kathmandu")

    # Get the current time in the local time zone
    now = timezone.localtime(timezone.now())
    print("Current Time (Local):", now)

    # Retrieve all appointments for the current user (patient)
    all_appointments = Appointment.objects.filter(patient=request.user)

    # Separate upcoming and past appointments based on date and time
    upcoming_appointments = all_appointments.filter(
        Q(appointment_date__gt=now.date()) | (Q(appointment_date=now.date()) & Q(appointment_time__gt=now.time()))
    )

    past_appointments = all_appointments.filter(
        Q(appointment_date__lt=now.date()) | (Q(appointment_date=now.date()) & Q(appointment_time__lte=now.time()))
    )

    # Pass the appointments to the template
    context = {
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
    }

    return render(request, 'my_appointment.html', context)


def cancel_appointment(request, appointment_id):
    # Retrieve the appointment object or return a 404 response if not found
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if the appointment belongs to the currently logged-in user
    if appointment.patient == request.user:
        # Delete the appointment
        appointment.delete()
        # Redirect to the My Appointments page or any other appropriate page
        return redirect('my_appointment')
    else:
        # If the appointment doesn't belong to the user, handle accordingly
        return render(request, 'error_page.html', {'message': 'Unauthorized access'})
    


def doctor_appointments(request):
    try:
        current_doctor = request.user.doctor  # Access the related Doctor profile
    except Doctor.DoesNotExist:
        current_doctor = None

    if current_doctor:
        # Fetch appointments for the current doctor
        completed_appointments = Appointment.objects.filter(doctor=current_doctor, status='complete')
        remaining_appointments = Appointment.objects.filter(doctor=current_doctor, status='remaining')
        
        # Pass appointments to the template
        context = {
            'completed_appointments': completed_appointments,
            'remaining_appointments': remaining_appointments,
        }

        return render(request, 'doctor_appointments.html', context)
    else:
        # Handle the case where the user is not a doctor
        return render(request, 'error.html', {'message': 'You are not a doctor.'})

def review(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Handle uploading new reports
        new_report_files = request.FILES.getlist('new_report_files')
        for new_report_file in new_report_files:
            NewReport.objects.create(appointment=appointment, report_file=new_report_file)

        # Handle updating appointment status
        new_status = 'complete' if request.POST.get('status') == 'on' else 'remaining'
        appointment.status = new_status
        appointment.save()

    return render(request, 'review.html', {'appointment': appointment})

   
def patient_list(request):
    # Exclude doctors and superusers
     
    patients = CustomUser.objects.filter(is_superuser=False, doctor__isnull=True)
    
    context = {'patients': patients}
    return render(request, 'patient_list.html', context)

# def add_doctor(request):
#     return render(request, 'add_doctor.html')

def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'edit_doctor.html', {'doctor': doctor})

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

# def delete_doctor(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     doctor.delete()
#     # You might want to add a success message or handle redirects appropriately.
#     return redirect('doctor_list')

def add_doctor(request):
    if request.method == 'POST':
        # Retrieve data from the form
        dusername = request.POST.get('dusername')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        demail = request.POST.get('demail')
        dcontact = request.POST.get('dcontact')
        dage = request.POST.get('dage')
        dsex = request.POST.get('dsex')
        daddress = request.POST.get('daddress')
        dpassword = request.POST.get('dpassword')

        # Check if the username, email, and contact are already used
        if CustomUser.objects.filter(username=dusername).exists():
            messages.error(request, "Username is already used.")
            return redirect('add_doctor')

        if CustomUser.objects.filter(email=demail).exists():
            messages.error(request, "Email is already used.")
            return redirect('add_doctor')

        if CustomUser.objects.filter(contact=dcontact).exists():
            messages.error(request, "Number is already used.")
            return redirect('add_doctor')

        # Create a CustomUser instance
        myuser = CustomUser.objects.create_user(dusername, demail, dpassword)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.age = dage
        myuser.contact = dcontact
        myuser.sex = dsex
        myuser.address = daddress

        # Check if 'profile_image' exists in request.FILES
        if 'profile_image' in request.FILES:
            myuser.profile_image = request.FILES['profile_image']

        myuser.save()

        # Create Doctor instance
        doctor = Doctor.objects.create(
        user=myuser,
        qualification=request.POST.get('qualification'),
        specialities=request.POST.get('specialities'),
        descriptions=request.POST.get('descriptions'),
        hospital=request.POST.get('dhospital'),
        start_time=request.POST.get('start_time'),
        end_time=request.POST.get('end_time'),
        break_start1=request.POST.get('break_start1'),
        break_end1=request.POST.get('break_end1'),
        break_start2=request.POST.get('break_start2'),
        break_end2=request.POST.get('break_end2'),
        is_booked=False
        )

        availability_days = request.POST.getlist('availability_days[]')
        
        for day in availability_days:
         doctor_availability, created = DoctorAvailability.objects.get_or_create(day=day)
         doctor.availability_days.add(doctor_availability) 
        

        # Save the doctor instance
        doctor.save()
        

        messages.success(request, "Doctor added successfully.")
        return redirect('doctor_list')

    return render(request, 'add_doctor.html')
