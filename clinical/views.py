from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from .models import Professional, Appointment
from .serializers import ProfessionalSerializer, AppointmentSerializer

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all().order_by('-created_at')
    serializer_class = ProfessionalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'occupation']

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('date')
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        professional_id = self.request.query_params.get('professional_id')
        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)
        return queryset
