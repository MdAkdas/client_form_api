from django.db import models


from django.utils import timezone
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from multiselectfield import MultiSelectField

from django.core.exceptions import ValidationError
import datetime
# Create your models here.

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    ROLE = (
		("Client",_("Client")),
	)

    role = models.CharField(max_length=8, choices=ROLE, default="Client")

    #serve as unique identifier 
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name or ''



def validate_date_in_past(value):
    today = datetime.date.today()
    if value < today:
        raise ValidationError('date is in the past')


def validate_time_range(value):
    minT = datetime.time(5,00,00)
    maxT = datetime.time(9,00,00)

    if value >maxT or value <minT:
        raise ValidationError('Shift Time range is 5am to 9 am')



class Shift(models.Model):
    clientName = models.ForeignKey(User, related_name='shifts',null=True, on_delete=models.SET_NULL)
    start_date=models.DateField(validators=[validate_date_in_past])

    arrival_time = models.TimeField(validators=[validate_time_range]) #we can validate in clean method also
    departure_time = models.TimeField(validators=[validate_time_range])

    REPEAT_SELECTION = (
        ('None',_('None')),
        ('Daily',_('Daily')),
        ('Weekly',_('Weekly')),
        )
    repeat = models.CharField(max_length=7,choices=REPEAT_SELECTION)
    
    SHIFT_OPTION = (
        ("5am to 9am", "5am to 9am"),
        )
    shift_availability = models.CharField(max_length=10,choices=SHIFT_OPTION, default="5am to 9am")
    
    DAYS_OF_WEEK = (
       ("Monday", "Monday"),
       ("Tuesday", "Tuesday"),
       ("Wednesday", "Wednesday"),
       ("Thursday", "Thursday"),
       ("Friday", "Friday"),
       ("Saturday", "Saturday"),
       ("Sunday", "Sunday"),
    )
    days = MultiSelectField(choices=DAYS_OF_WEEK)
    weekdaysOnly = models.BooleanField(default=True)

    def clean(self):
        if self.arrival_time > self.departure_time:
            raise ValidationError('Arrival Time must be before departure Time')
        
        if self.weekdaysOnly == True:
            if "Saturday" in self.days or "Sunday" in self.days:
                raise ValidationError('Weekdays Only Selected.')