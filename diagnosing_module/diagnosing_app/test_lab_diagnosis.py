import pytest
import pytest_asyncio
from django.urls import reverse
from django.test import AsyncClient
from datetime import datetime

import json
from datetime import datetime, date
from .models import Patient, MedirevOrderRequest, Doctor, MedirevResult

@pytest.mark.django_db
@pytest.mark.asyncio(loop_scope="session")
class TestMedirevDiagnosisEndpoints:
    @pytest_asyncio.fixture(autouse=True,loop_scope="session",scope="function")
    async def setup_test_data(self):
        """Fixture that runs before each test"""
        # Define the test patient data
       
        self.test_patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "M",
            "contact_number": "1234567890",
            "email": "john@example.com"
        }

        self.test_doctor_data = {
            "first_name": "John",
            "last_name": "Doe",
            "specialty": "Optometry"
           
        }
        
      

        # Initialize AsyncClient
        self.client = AsyncClient()
        
        # return self  # Return self to make instance attributes avaiMedirevle
    
        # Cleanup will happen automatically due to django_db mark

    # Rest of the test methods remain the same
    # @pytest.mark.asyncio
    async def test_create_patient(self,request):
        """Test creating a new patient"""
        test_data = self.test_patient_data

        
        url = reverse('create-patient')
        response = await self.client.post(
            url,
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # assert response.status_code == 201
        data = response.json()
        # print("the error is",data)
        request.session.data=data
      
        
        # print("this is response patient data",data) 
        assert data['first_name'] ==  test_data['first_name']
        assert data['last_name'] ==  test_data['last_name']


    # @pytest.mark.asyncio
    async def test_get_patient(self,request):
        """Test retrieving a patient"""
       
        patient = request.session.data
        # print("id",patient_id)
        url = reverse('get-patient', kwargs={'patient_id': patient.get('id')})
        response = await self.client.get(url)

        
        assert response.status_code == 200
        data = response.json()
        # print("this is response patient data",data)
        assert data['first_name'] == patient.get("first_name")
        assert data['last_name'] == patient.get("last_name")

    async def test_create_doctor(self,request):
        """Test creating a new doctor"""
        test_data = self.test_doctor_data
        # test_data['email'] = "john1.new@example.com"
        # print(self.test_patient_data)
        
        url = reverse('create-doctor')
        response = await self.client.post(
            url,
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # assert response.status_code == 201
        data1 = response.json()
        # print("the error is",data)
        request.session.data1=data1
      
        
        print("this is response doctor data",data1) 
        assert data1['first_name'] ==  test_data['first_name']
        assert data1['last_name'] ==  test_data['last_name']
    
    async def test_get_doctor(self,request):
        """Test retrieving a doctor"""
       
        doctor = request.session.data1
        # print("id",patient_id)
        url = reverse('get-doctor', kwargs={'doctor_id': doctor.get('id')})
        response = await self.client.get(url)

        
        assert response.status_code == 200
        data = response.json()
        print("this is get response doctor data",data)
        assert data['first_name'] == doctor.get("first_name")
        assert data['last_name'] == doctor.get("last_name")

    # @pytest.mark.asyncio
    async def test_create_Medirev_order(self,request):
        """Test creating a Medirev order request"""
        url = reverse('create-Medirevorder-request')
        patient = request.session.data
        data = {
            "patient_id": patient.get("id"),
            "test_name": "Blood Test",
            "requested_date": datetime.now().date().isoformat()
        }
        print("data",data)
        response = await self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        response_data = response.json()
        request.session.order_request = response_data
        # print("err occured",response_data)
        assert response_data['test_name'] == data['test_name']

    # @pytest.mark.asyncio
    async def test_get_Medirev_order(self,request):
        """Test retrieving a Medirev order request"""
        Medirev_request = request.session.order_request
        url = reverse('get-Medirevorder-request', kwargs={'order_id': Medirev_request.get("id")})
        print(url)
        response = await self.client.get(url)
        
        
        # assert response.status_code == 200
        data = response.json()
        print("Medirev data",data)        
        # assert data['test_name'] == self.Medirev_order.test_name

    # @pytest.mark.asyncio
    async def test_create_Medirev_result(self,request):
        """Test creating a Medirev result"""
        url = reverse('create-Medirev-results')
        Medirev_request = request.session.order_request
        doctor = request.session.data1
        data = {
            "Medirev_order_id": Medirev_request.get("id"),
            "doctor_id": doctor.get("id"),
            "result": "Normal"
        }
        
        response = await self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # assert response.status_code == 201
        response_data = response.json()
        request.session.Medirev_result = response_data
        print("results",response_data)
        assert response_data['result'] == data['result']

    # @pytest.mark.asyncio
    async def test_get_Medirev_result(self,request):
        """Test retrieving a Medirev result"""
        Medirevresult = request.session.Medirev_result
        url = reverse('get-Medirev-result', kwargs={'Medirev_result_id': Medirevresult.get("id")})
        print(url)
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        print("get Medirevresult",data)
        assert data['result'] == Medirevresult.get("result")

    # @pytest.mark.asyncio
    async def test_create_Medirev_report(self,request):
        """Test creating a Medirev report"""
        url = reverse('create-Medirev-report')
        Medirevresult = request.session.Medirev_result 
        data = {
            "Medirev_result_id": Medirevresult.get("id"),
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
        request.session.Medirevreport= response_data
        print("report",response_data)
        assert response_data['report_data'] == data['report_data']
        assert response_data['shared_with_doctor'] == data['shared_with_doctor']

    # @pytest.mark.asyncio
    async def test_get_Medirev_report(self,request):
        """Test retrieving a Medirev report"""
        Medirevreport = request.session.Medirevreport
        url = reverse('get-Medirev-reports', kwargs={'Medirev_report_id': Medirevreport.get("id")})
        response = await self.client.get(url)
        
        assert response.status_code == 200
        data = response.json()
        print("Medirevrepor",data)
        # assert data['Medirev_result'] == Medirevreport.get.id
        assert data['report_data'] == Medirevreport.get("report_data")
        assert 'generated_at' in data
        assert data['shared_with_doctor'] is True