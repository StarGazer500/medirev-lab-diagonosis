from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import LabOrderRequest, Patient, Doctor,LabResult,LabReport
from django.shortcuts import get_object_or_404
import json


# @method_decorator(csrf_exempt, name='dispatch')
class CreatePatientView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            date_of_birth = data.get('date_of_birth')
            gender = data.get('gender')
            contact_number = data.get('contact_number')
            email = data.get('email')

            # Create a new patient
            patient = await Patient.objects.acreate(
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender,
                contact_number=contact_number,
                email=email
            )

            response_data = {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "date_of_birth": patient.date_of_birth.isoformat(),
                "gender": patient.gender,
                "contact_number": patient.contact_number,
                "email": patient.email,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Async view to retrieve a Patient
class GetPatientView(View):
    async def get(self, request, *args, **kwargs):
        patient_id = kwargs.get('patient_id')
        try:
            patient = await Patient.objects.aget(id=patient_id)
            
            response_data = {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "date_of_birth": patient.date_of_birth.isoformat(),
                "gender": patient.gender,
                "contact_number": patient.contact_number,
                "email": patient.email,
            }
            return JsonResponse(response_data)
        except Patient.DoesNotExist:
            return JsonResponse({"error": "Patient not found"}, status=404)



# Async view to create a LabOrderRequest
# @method_decorator(csrf_exempt, name='dispatch')
class CreateLabOrderRequestView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            patient_id = data.get('patient_id')
            # doctor_id = data.get('doctor_id')
            test_name = data.get('test_name')
            requested_date = data.get('requested_date')

            # Fetch the patient and doctor from DB
            patient = await Patient.objects.aget(id=patient_id)  # Async ORM query
            # doctor = await Doctor.objects.aget(id=doctor_id)

            # Create the lab order request
            lab_order_request = await LabOrderRequest.objects.acreate(
                patient=patient,
                # doctor=doctor,
                test_name=test_name,
                requested_date=requested_date,
            )

            response_data = {
                "id": lab_order_request.id,
                "patient": str(lab_order_request.patient),
                "doctor": str(lab_order_request.doctor),
                "test_name": lab_order_request.test_name,
                "status": lab_order_request.status,
                "requested_date": lab_order_request.requested_date.isoformat(),
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


#Async view to Retrieve a LabOrderRequest
class GetLabOrderRequestView(View):
    async def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            lab_order_request = await LabOrderRequest.objects.aget(id=order_id)
            
            response_data = {
                "id": lab_order_request.id,
                "patient": str(lab_order_request.patient),
                # "doctor": str(lab_order_request.doctor),
                "test_name": lab_order_request.test_name,
                "status": lab_order_request.status,
                "requested_date": lab_order_request.requested_date.isoformat(),
                "order_date": lab_order_request.order_date.isoformat(),
            }
            return JsonResponse(response_data,status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        

# Async view to create a LabResult
# @method_decorator(csrf_exempt, name='dispatch')
class CreateLabResultView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            lab_order_id = data.get('lab_order_id')
            doctor_id = data.get('doctor_id')
            result = data.get('result')

            # Fetch the LabOrderRequest and Doctor
            lab_order = await LabOrderRequest.objects.aget(id=lab_order_id)
            doctor = await Doctor.objects.aget(id=doctor_id)

            # Create the LabResult instance
            lab_result = await LabResult.objects.acreate(
                lab_order=lab_order,
                doctor=doctor,
                result=result
            )

            response_data = {
                "id": lab_result.id,
                "lab_order": lab_result.lab_order.id,
                "doctor": str(lab_result.doctor),
                "result": lab_result.result,
                "test_date": lab_result.test_date.isoformat(),
                "created_at": lab_result.created_at.isoformat(),
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Async view to retrieve a LabResult
class GetLabResultView(View):
    async def get(self, request, *args, **kwargs):
        lab_result_id = kwargs.get('lab_result_id')
        try:
            lab_result = await LabResult.objects.aget(id=lab_result_id)
            
            response_data = {
                "id": lab_result.id,
                "lab_order": lab_result.lab_order.id,
                "doctor": str(lab_result.doctor),
                "result": lab_result.result,
                "test_date": lab_result.test_date.isoformat(),
                "created_at": lab_result.created_at.isoformat(),
            }
            return JsonResponse(response_data)
        except LabResult.DoesNotExist:
            return JsonResponse({"error": "Lab result not found"}, status=404)
        

@method_decorator(csrf_exempt, name='dispatch')
class CreateLabReportView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            lab_result_id = data.get('lab_result_id')
            report_data = data.get('report_data')
            shared_with_doctor = data.get('shared_with_doctor', False)

            # Fetch the LabResult
            lab_result = await LabResult.objects.aget(id=lab_result_id)

            # Create the LabReport instance
            lab_report = await LabReport.objects.acreate(
                lab_result=lab_result,
                report_data=report_data,
                shared_with_doctor=shared_with_doctor
            )

            response_data = {
                "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "report_data": lab_report.report_data,
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
            }
            return JsonResponse(response_data, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Async view to retrieve a LabReport
class GetLabReportView(View):
    async def get(self, request, *args, **kwargs):
        lab_report_id = kwargs.get('lab_report_id')
        try:
            lab_report = await LabReport.objects.aget(id=lab_report_id)
            
            response_data = {
                "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "report_data": lab_report.report_data,
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
            }
            return JsonResponse(response_data)
        except LabReport.DoesNotExist:
            return JsonResponse({"error": "Lab report not found"}, status=404)