from rest_framework import serializers

from .models import Shift

class ShiftSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Shift
		exclude = ['id']

	def validate(self,attrs):
		instance = Shift(**attrs)
		instance.clean()
		return attrs