import pytest
from django.urls import reverse
from django.test import AsyncClient

import json
from datetime import datetime, date
from .models import Patient, LabOrderRequest, Doctor, LabResult


@pytest.mark.django_db
@pytest.mark.asyncio
class TestLabDiagnosisEndpoints:
    async def setup_method(self):
        """Setup method that runs before each test"""
        # Define the test patient data here
        self.test_patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "contact_number": "1234567890",
            "email": "john@example.com"
        }
        
        # Create test patient
        self.patient = await Patient.objects.acreate(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            contact_number="1234567890",
            email="john@example.com"
        )
        
        # Create test doctor
        self.doctor = await Doctor.objects.acreate(
            first_name="Dr",
            last_name="Smith",
            specialization="General"
        )
        
        # Create test lab order
        self.lab_order = await LabOrderRequest.objects.acreate(
            patient=self.patient,
            test_name="Blood Test",
            requested_date=datetime.now().date()
        )
        
        # Create test lab result
        self.lab_result = await LabResult.objects.acreate(
            lab_order=self.lab_order,
            doctor=self.doctor,
            result="Normal"
        )

        # Initialize AsyncClient
        self.client = AsyncClient()

    async def test_create_patient(self):
        """Test creating a new patient"""
        url = reverse('create-patient')
        response = await self.client.post(
            url,
            data=json.dumps(self.test_patient_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['first_name'] == self.test_patient_data['first_name']
        assert data['last_name'] == self.test_patient_data['last_name']

    async def test_get_patient(self):
        """Test retrieving a patient"""
        url = reverse('get-patient', kwargs={'patient_id': self.patient.id})
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['first_name'] == self.patient.first_name
        assert data['last_name'] == self.patient.last_name

    async def test_create_lab_order(self):
        """Test creating a lab order request"""
        url = reverse('create-laborder-request')
        data = {
            "patient_id": self.patient.id,
            "test_name": "Blood Test",
            "requested_date": datetime.now().date().isoformat()
        }
        
        response = await self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data['test_name'] == data['test_name']

    async def test_get_lab_order(self):
        """Test retrieving a lab order request"""
        url = reverse('get-laborder-request', kwargs={'order_id': self.lab_order.id})
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['test_name'] == self.lab_order.test_name

    async def test_create_lab_result(self):
        """Test creating a lab result"""
        url = reverse('create-lab-results')
        data = {
            "lab_order_id": self.lab_order.id,
            "doctor_id": self.doctor.id,
            "result": "Normal"
        }
        
        response = await self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data['result'] == data['result']

    async def test_get_lab_result(self):
        """Test retrieving a lab result"""
        url = reverse('get-lab-request', kwargs={'lab_result_id': self.lab_result.id})
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['result'] == self.lab_result.result

    async def test_create_lab_report(self):
        """Test creating a lab report"""
        url = reverse('create-lab-report')
        data = {
            "lab_result_id": self.lab_result.id,
            "report_data": "Blood test shows normal levels.",
            "shared_with_doctor": True
        }
        
        response = await self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data['report_data'] == data['report_data']
        assert response_data['shared_with_doctor'] == data['shared_with_doctor']

    async def test_get_lab_report(self):
        """Test retrieving a lab report"""
        url = reverse('get-lab-reports', kwargs={'lab_report_id': self.lab_result.id})
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert data['lab_result'] == self.lab_result.id
        assert data['report_data'] == self.lab_result.result
        assert 'generated_at' in data  # Check if the generated_at field exists
        assert data['shared_with_doctor'] is False  # Default value should be False for newly created report
