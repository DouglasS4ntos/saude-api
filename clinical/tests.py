from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Professional, Appointment
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ClinicalAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.professional = Professional.objects.create(
            full_name="Dr. Teste Lacrei",
            occupation="Psicologia",
            address="Rua da Inclusão, 500",
            contact="teste@lacrei.com"
        )

        self.list_url = reverse('professional-list')
        self.appointment_url = reverse('appointment-list')

    def test_create_professional(self):
        data = {
            "full_name": "Nova Pessoa Médica",
            "occupation": "Endocrinologia",
            "address": "Av. Brasil, 100",
            "contact": "medica@lacrei.com"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 2)

    # 2. Teste de Erro (Dado Ausente - Requisito do Edital)
    def test_create_professional_invalid_data(self):
        data = {"full_name": ""}  # Nome vazio
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 3. Teste de Busca por ID de Profissional (Requisito Eliminatório)
    def test_filter_appointments_by_professional(self):
        # Cria uma consulta para o profissional
        Appointment.objects.create(professional=self.professional, date=timezone.now())
        response = self.client.get(self.appointment_url, {'professional_id': self.professional.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['professional'], self.professional.id)
