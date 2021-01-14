from django.urls import path
from .views import Shifts, CreateShift

app_name = 'staff'


urlpatterns = [
    path('shifts/', Shifts.as_view(), name='shifts'),
    path('create/', CreateShift.as_view(), name='create'),
]