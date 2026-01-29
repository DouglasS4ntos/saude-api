from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Professional, Appointment
from .serializers import ProfessionalSerializer, AppointmentSerializer
import logging

logger = logging.getLogger(__name__)

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all().order_by('-created_at')
    serializer_class = ProfessionalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'occupation']

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f" [AUDITORIA] Profissional cadastrado: {instance.full_name} (ID: {instance.id}) pelo usuário {self.request.user}")

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('date')
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        professional_id = self.request.query_params.get('professional_id')
        if professional_id:
            queryset = queryset.filter(professional_id=professional_id)
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f" [AUDITORIA] Nova consulta agendada para o Profissional ID: {instance.professional.id}")
