from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


    
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    qualification = models.CharField(max_length=100)
    specialities = models.CharField(max_length=100)
    descriptions = models.TextField()
    hospital=models.TextField()
    availability_days = models.ManyToManyField('DoctorAvailability',related_name='doctors')
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_start1 = models.TimeField()
    break_end1 = models.TimeField()
    break_start2 = models.TimeField()
    break_end2 = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.qualification}"

class DoctorAvailability(models.Model):
    day = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.day




class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=15, default='remaining')
    old_reports = models.FileField(upload_to='old_reports/', null=True, blank=True)

    def __str__(self):
        return f"Appointment for {self.doctor.user.username} on {self.appointment_date} at {self.appointment_time}"
    
class NewReport(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='new_reports', on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='new_reports/')

    def __str__(self):
        return f"New Report for Appointment {self.appointment.id}"    