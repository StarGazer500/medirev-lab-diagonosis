from django.http import JsonResponse
from django.db import IntegrityError
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
                "date_of_birth": patient.date_of_birth,
                "gender": patient.gender,
                "contact_number": patient.contact_number,
                "email": patient.email,
            }
            return JsonResponse(response_data, status=201)
        
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The email is already in use. Please provide a unique email."}, status=400)
            else:
                print("different int")
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
      
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)



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
                "date_of_birth": patient.date_of_birth,
                "gender": patient.gender,
                "contact_number": patient.contact_number,
                "email": patient.email,
            }
            return JsonResponse(response_data)
        except Patient.DoesNotExist:
            return JsonResponse({"error": "Patient not found"}, status=404)
        
        



class CreateDoctorView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            specialty = data.get('specialty')
            

            # Create a new patient
            doctor = await Doctor.objects.acreate(
                first_name=first_name,
                last_name=last_name,
                specialty = specialty
            
            )

            response_data = {
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "specialty": doctor.specialty
              
            }
            return JsonResponse(response_data, status=201)
      
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The email is already in use. Please provide a unique email."}, status=400)
            else:
                print("different int")
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)


# Async view to retrieve a Patient
class GetDoctorView(View):
    async def get(self, request, *args, **kwargs):
        doctor_id = kwargs.get('doctor_id')
        try:
            doctor = await Doctor.objects.aget(id=doctor_id)
            
            response_data = {
                "id": doctor.id,
                "first_name": doctor.first_name,
                "last_name": doctor.last_name,
                "specialty": doctor.specialty
              
            }
            return JsonResponse(response_data,status = 200)
        except Patient.DoesNotExist:
            return JsonResponse({"error": "Doctor not found"}, status=404)


# Async view to create a LabOrderRequest
# @method_decorator(csrf_exempt, name='dispatch')
class CreateLabOrderRequestView(View):
    async def post(self, request, *args, **kwargs):
        print("reached",json.loads(request.body))
        try:
            data = json.loads(request.body)
            
            # Extract patient data from the request
            patient_data = {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'date_of_birth': data.get('date_of_birth'),
                'gender': data.get('gender'),
                'contact_number': data.get('contact_number'),
                'email': data.get('email')
            }

             # Extract lab order data
            test_description = data.get('test_description')
            requested_date = data.get('requested_date')
            
            # Create patient record
            patient = await Patient.objects.acreate(**patient_data)
            
            # Create the lab order request with the newly created patient
            lab_order_request = await LabOrderRequest.objects.acreate(
                patient=patient,
                test_description=test_description,
                requested_date=requested_date,
            )
            
            response_data = {
                "id": lab_order_request.id,
                "patient": f"{patient.first_name} {patient.last_name}",
                "test_description": lab_order_request.test_description,
                "request_status": lab_order_request.request_status,
                "requested_date": lab_order_request.requested_date,
            }
            return JsonResponse(response_data, status=201)
        
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The email is already in use. Please provide a unique email."}, status=400)
            else:
                print("different int")
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)

# GetLabOrderRequestView remains mostly the same, but let's fix the field name
class GetLabOrderRequestView(View):
    async def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            lab_order_request = await LabOrderRequest.objects.select_related('patient').aget(id=order_id)
            response_data = {
                "id": lab_order_request.id,
                "patient": f"{lab_order_request.patient.first_name} {lab_order_request.patient.last_name}",
                "test_description": lab_order_request.test_description,
                "status": lab_order_request.status,
                "requested_date": lab_order_request.requested_date,
                "order_date": lab_order_request.order_date,
            }
            return JsonResponse(response_data, status=200)
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
    
        
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The email is already in use. Please provide a unique email."}, status=400)
            else:
                print("different int")
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)



# Async view to retrieve a LabResult
class GetLabResultView(View):
    async def get(self, request, *args, **kwargs):
        lab_result_id = kwargs.get('lab_result_id')
        try:
            lab_result = await LabResult.objects.select_related('lab_order','doctor').aget(id=lab_result_id)
            
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
        

# @method_decorator(csrf_exempt, name='dispatch')
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
    
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The email is already in use. Please provide a unique email."}, status=400)
            else:
                print("different int")
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)



# Async view to retrieve a LabReport
class GetLabReportView(View):
    async def get(self, request, *args, **kwargs):
        lab_report_id = kwargs.get('lab_report_id')
        try:
            lab_report = await LabReport.objects.select_related('lab_result').aget(id=lab_report_id)
            
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