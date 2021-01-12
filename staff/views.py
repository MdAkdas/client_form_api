from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from .models import Shift
from .serializers import ShiftSerializer 





class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class Shifts(generics.ListAPIView):
	permission_classes = (IsAuthenticated,)
	
	serializer_class = ShiftSerializer
	queryset = Shift.objects.all()

class CreateShift(generics.CreateAPIView):

	permission_classes=(IsAuthenticated,)
	serializer_class=ShiftSerializer
