from django.urls import path
from .views import HelloView, Shifts, CreateShift

app_name = 'staff'


urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('shifts/', Shifts.as_view(), name='shifts'),
    path('create/', CreateShift.as_view(), name='create'),
]