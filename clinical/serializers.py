from rest_framework import serializers
from django.utils.html import escape
from .models import Professional, Appointment

class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'

    def validate(self, data):
        for field in ['full_name', 'occupation', 'address', 'contact']:
            if field in data:
                data[field] = escape(data[field])
        return data

class AppointmentSerializer(serializers.ModelSerializer):
    professional_name = serializers.ReadOnlyField(source='professional.full_name')

    class Meta:
        model = Appointment
        fields = '__all__'
