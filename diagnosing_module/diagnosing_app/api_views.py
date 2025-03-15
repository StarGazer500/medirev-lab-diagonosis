from django.http import JsonResponse
from django.db import IntegrityError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import LabOrderRequest, Patient, Doctor,LabResult,LabReport
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import sync_to_async


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


class GetAllPatientView(View):
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch all patients
            patients = await sync_to_async(list)(Patient.objects.all())
            print(patients)
            # Prepare the response data
            response_data = [
                {
                    "id": patient.id,
                    "first_name": patient.first_name,
                    "last_name": patient.last_name,
                    "date_of_birth": patient.date_of_birth,
                    "gender": patient.gender,
                    "contact_number": patient.contact_number,
                    "email": patient.email,
                }
                for patient in patients
            ]
            return JsonResponse(response_data, safe=False)  # safe=False allows the list as JSON
        except Exception as e:
            print("error is ",e)
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

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

    async def put(self, request, *args, **kwargs):
        patient_id = kwargs.get('patient_id')
        try:
            patient = await Patient.objects.aget(id=patient_id)
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Update patient fields if they are provided in the request
            patient.first_name = data.get('first_name', patient.first_name)
            patient.last_name = data.get('last_name', patient.last_name)
            patient.date_of_birth = data.get('date_of_birth', patient.date_of_birth)
            patient.gender = data.get('gender', patient.gender)
            patient.contact_number = data.get('contact_number', patient.contact_number)
            patient.email = data.get('email', patient.email)
            
            # Save the updated patient
            await patient.asave()
            
            # Prepare response with updated data
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
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    async def delete(self, request, *args, **kwargs):
        patient_id = kwargs.get('patient_id')
        try:
            # Try to get the patient object to delete
            patient = await Patient.objects.aget(id=patient_id)
            
            # Delete the patient
            await patient.adelete()
            
            # Return success response
            return JsonResponse({"message": "Patient deleted successfully"}, status=200)
        except Patient.DoesNotExist:
            return JsonResponse({"error": "Patient not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        



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


class GetAllDoctorView(View):
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch all patients
            doctors = await sync_to_async(list)(Doctor.objects.all())
            
            # Prepare the response data
            response_data = [
                {
                    "id": doctor.id,
                    "first_name": doctor.first_name,
                    "last_name": doctor.last_name,
                    "specialty": doctor.specialty
                }
                for doctor in doctors
            ]
            return JsonResponse(response_data, safe=False)  # safe=False allows the list as JSON
        except Exception as e:
            print("error is ",e)
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


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
                'email': data.get('email'),
               
            }

             # Extract lab order data
            test_description = data.get('test_description')
            requested_date = data.get('requested_date')
            
           
            
            # check if patient exist or create one
            patient, created = await Patient.objects.aget_or_create(
                email=patient_data.get("email"),
                defaults=patient_data
            )
            print("patient retrieved", patient)

             # check if order exist
            try:
                existing_order = await LabOrderRequest.objects.select_related('patient').aget(patient_id=patient.id)
                print(existing_order)
                return JsonResponse({
                    "message": "This lab order request already exists",
                    "id": existing_order.id
                }, status=400)
            except LabOrderRequest.DoesNotExist:
                # If the order does not exist, continue to create a new one
                pass

           
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
                return JsonResponse({"message": "This Appointment has been created already. Please provide a unique email."}, status=400)
            else:
                print("different integrity",e)
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)






class GetLabOrderRequestView(View):

    # GET method to retrieve lab order request details
    async def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            lab_order_request = await LabOrderRequest.objects.select_related('patient').aget(id=order_id)
            response_data = {
                "id": lab_order_request.id,
                "patient": f"{lab_order_request.patient.first_name} {lab_order_request.patient.last_name}",
                "test_description": lab_order_request.test_description,
                "status": lab_order_request.request_status,
                "requested_date": lab_order_request.requested_date,
                "order_date": lab_order_request.order_date,
            }
            return JsonResponse(response_data, status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

    # PUT method to update an existing lab order request
    async def put(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            lab_order_request = await LabOrderRequest.objects.select_related('patient').aget(id=order_id)
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Update fields if they are provided in the request
            lab_order_request.test_description = data.get('test_description', lab_order_request.test_description)
            lab_order_request.request_status = data.get('request_status', lab_order_request.request_status)
     
           

            # Save the updated lab order request
            await lab_order_request.asave()

            # Prepare response with updated data
            response_data = {
                "id": lab_order_request.id,
                "patient": f"{lab_order_request.patient.first_name} {lab_order_request.patient.last_name}",
                "test_description": lab_order_request.test_description,
                "status": lab_order_request.request_status,
                "requested_date": lab_order_request.requested_date,
                "order_date": lab_order_request.order_date,
            }
            return JsonResponse(response_data, status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("error",e)
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to remove a lab order request
    async def delete(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            # Try to get the lab order request object to delete
            lab_order_request = await LabOrderRequest.objects.aget(id=order_id)
            
            # Delete the lab order request
            await lab_order_request.adelete()
            
            # Return success response
            return JsonResponse({"message": "Lab order request deleted successfully"}, status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class ApproveLabRequest(View):

  

    # PUT method to update an existing lab order request
    async def put(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            lab_order_request = await LabOrderRequest.objects.select_related('patient').aget(id=order_id)
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Update fields if they are provided in the request
            
            lab_order_request.request_status = data.get('request_status', lab_order_request.request_status)
     
           

            # Save the updated lab order request
            await lab_order_request.asave()

            # Prepare response with updated data
            response_data = {
                "id": lab_order_request.id,
                "patient": f"{lab_order_request.patient.first_name} {lab_order_request.patient.last_name}",
                "test_description": lab_order_request.test_description,
                "status": lab_order_request.request_status,
                "requested_date": lab_order_request.requested_date,
                "order_date": lab_order_request.order_date,
            }
            return JsonResponse(response_data, status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("error",e)
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to remove a lab order request
    async def delete(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            # Try to get the lab order request object to delete
            lab_order_request = await LabOrderRequest.objects.aget(id=order_id)
            
            # Delete the lab order request
            await lab_order_request.adelete()
            
            # Return success response
            return JsonResponse({"message": "Lab order request deleted successfully"}, status=200)
        except LabOrderRequest.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



class GetAllLabOrderRequestView(View):
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch all Lab Requests with related patient data
            labrequests = await sync_to_async(list)(
                LabOrderRequest.objects.select_related('patient').all()
            )
            
            # Prepare the response data
            response_data = [
                {
                    "id": labrequest.id,
                    "patient": f"{labrequest.patient.first_name} {labrequest.patient.last_name}",
                    "test_description": labrequest.test_description,
                    "request_status": labrequest.request_status,
                    "requested_date": labrequest.requested_date,
                    "order_date": labrequest.order_date,
                }
                for labrequest in labrequests
            ]
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print("error is ", e)
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)


# Async view to create a LabResult
# @method_decorator(csrf_exempt, name='dispatch')
class CreateLabResultView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("data",data)
            lab_order_id = data.get('lab_order_id')
            
            result = data.get('result')

            # Fetch the LabOrderRequest and Doctor
            lab_order = await LabOrderRequest.objects.select_related('patient').aget(id=lab_order_id)
            
            

            # Create the LabResult instance
            lab_result = await LabResult.objects.acreate(
                lab_order=lab_order,
                result=result
            )

            response_data = {
                "id": lab_result.id,
                "lab_order": lab_result.lab_order.id,
                
                "result": lab_result.result,
                "test_date": lab_result.test_date.isoformat(),
                "created_at": lab_result.created_at.isoformat(),
            }
            return JsonResponse(response_data, status=201)
    
        
        except IntegrityError as e:
            print("intergrity")
            # Handle unique constraint errors or other integrity errors
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The Lab Result has been created already. Please provide a unique Order Id."}, status=400)
            else:
                print("different integrity",e)
                
                # If it's another integrity error, log the error and return a generic message
                return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:

            # Log the exception for debugging (use logging in production)
            print(str(e))  # In production, use a proper logging mechanism
            
            # Return a generic error message
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)



# Async view to retrieve a LabResult
class GetLabResultView(View):
    # GET method to retrieve lab result details
    async def get(self, request, *args, **kwargs):
        lab_result_id = kwargs.get('lab_result_id')
        try:
            lab_result = await LabResult.objects.select_related('lab_order').aget(id=lab_result_id)
            
            response_data = {
                "id": lab_result.id,
                "lab_order": lab_result.lab_order.id,
                "result": lab_result.result,
                "test_date": lab_result.test_date.isoformat(),
                "created_at": lab_result.created_at.isoformat(),
            }
            return JsonResponse(response_data)
        except LabResult.DoesNotExist:
            return JsonResponse({"error": "Lab result not found"}, status=404)

    # PUT method to update an existing lab result
    async def put(self, request, *args, **kwargs):
        lab_result_id = kwargs.get('lab_result_id')
        try:
            lab_result = await LabResult.objects.select_related('lab_order').aget(id=lab_result_id)
            
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Update fields if they are provided in the request
            lab_result.result = data.get('result', lab_result.result)
           
            
            # Save the updated lab result
            await lab_result.asave()

            # Prepare response with updated data
            response_data = {
                "id": lab_result.id,
                "lab_order": lab_result.lab_order.id,
                "result": lab_result.result,
                "test_date": lab_result.test_date.isoformat(),
                "created_at": lab_result.created_at.isoformat(),
            }
            return JsonResponse(response_data, status=200)
        except LabResult.DoesNotExist:
            return JsonResponse({"error": "Lab result not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("error", e)
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to remove a lab result
    async def delete(self, request, *args, **kwargs):
        lab_result_id = kwargs.get('lab_result_id')
        try:
            # Try to get the lab result object to delete
            lab_result = await LabResult.objects.aget(id=lab_result_id)
            
            # Delete the lab result
            await lab_result.adelete()
            
            # Return success response
            return JsonResponse({"message": "Lab result deleted successfully"}, status=200)
        except LabResult.DoesNotExist:
            return JsonResponse({"error": "Lab result not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class GetAllLabResultView(View):
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch all Lab Requests with related patient data
            lab_results = await sync_to_async(list)(
                LabResult.objects.select_related('lab_order').all()
            )
            
            # Prepare the response data
            response_data = [
                {
                    "id": lab_result.id,
                    "lab_order": lab_result.lab_order.id,
                   
                    "result": lab_result.result,
                    "test_date": lab_result.test_date.isoformat(),
                    "created_at": lab_result.created_at.isoformat(),
                }
                for lab_result in lab_results
            ]
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print("error is ", e)
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        


# @method_decorator(csrf_exempt, name='dispatch')
class CreateLabReportView(View):
    async def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("data", data)
            lab_result_id = data.get('lab_result_id')
            doctor_id = data.get('doctor_id')
            report_data = data.get('report_data')
            shared_with_doctor = data.get('shared_with_doctor', False)

            # Fetch the LabResult and Doctor
            lab_result = await LabResult.objects.select_related('lab_order').aget(id=lab_result_id)
            doctor = await Doctor.objects.aget(id=doctor_id)

            # Create the LabReport instance
            lab_report = await LabReport.objects.acreate(
                doctor=doctor,
                lab_result=lab_result,
                report_data=report_data,
                shared_with_doctor=shared_with_doctor
            )

            # Generate and save PDF report
            await sync_to_async(lab_report.generate_pdf_report)()  # Wrap synchronous call
            await lab_report.asave()  # Save the instance with the PDF file

            response_data = {
                "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "doctor": f"{lab_report.doctor.first_name} {lab_report.doctor.last_name}",
                "report_data": lab_report.report_data,
                "report_file": lab_report.report_file.url if lab_report.report_file else None,
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
            }
            return JsonResponse(response_data, status=201)
    
        except IntegrityError as e:
            print("integrity error:", str(e))
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({"message": "The report has already been generated. Please provide a different ID."}, status=400)
            return JsonResponse({"message": "An error occurred while processing your request. Please try again."}, status=400)

        except Exception as e:
            print("error:", str(e))
            return JsonResponse({"message": "An unexpected error occurred. Please try again later."}, status=500)



class GetLabReportView(View):
    # GET method to retrieve lab report details
    async def get(self, request, *args, **kwargs):
        lab_report_id = kwargs.get('lab_report_id')
        try:
            lab_report = await LabReport.objects.select_related('lab_result', 'doctor').aget(id=lab_report_id)
            
            response_data = {
                "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "report_file": lab_report.report_file.url if lab_report.report_file else None,
                "report_data": lab_report.report_data,
                "doctor_id": lab_report.doctor.id,
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
            }
            return JsonResponse(response_data)
        except LabReport.DoesNotExist:
            return JsonResponse({"error": "Lab report not found"}, status=404)

    # PUT method to update an existing lab report
    async def put(self, request, *args, **kwargs):
        lab_report_id = kwargs.get('lab_report_id')
        try:
            lab_report = await LabReport.objects.select_related('lab_result', 'doctor').aget(id=lab_report_id)

            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Update fields if they are provided in the request
            lab_report.report_data = data.get('report_data', lab_report.report_data)
            lab_report.shared_with_doctor = data.get('shared_with_doctor', lab_report.shared_with_doctor)

            # Optionally update doctor if provided
            doctor_id = data.get('doctor_id')
            if doctor_id:
                doctor = await Doctor.objects.aget(id=doctor_id)
                lab_report.doctor = doctor

            # Save the updated lab report
            
            await lab_report.asave()

            await sync_to_async(lab_report.generate_pdf_report)()  # Wrap synchronous call in sync_to_async
            await lab_report.asave()

            # Prepare the response with updated data
            response_data = {
                "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "report_data": lab_report.report_data,
                "doctor": f"{lab_report.doctor.first_name} {lab_report.doctor.last_name}",
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
            }
            return JsonResponse(response_data, status=200)
        except LabReport.DoesNotExist:
            return JsonResponse({"error": "Lab report not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            print("error", e)
            return JsonResponse({"error": str(e)}, status=500)

    # DELETE method to remove a lab report
    async def delete(self, request, *args, **kwargs):
        lab_report_id = kwargs.get('lab_report_id')
        try:
            # Try to get the lab report object to delete
            lab_report = await LabReport.objects.aget(id=lab_report_id)
            
            # Delete the lab report
            await lab_report.adelete()
            
            # Return success response
            return JsonResponse({"message": "Lab report deleted successfully"}, status=200)
        except LabReport.DoesNotExist:
            return JsonResponse({"error": "Lab report not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class GetAllLabReportView(View):
    async def get(self, request, *args, **kwargs):
        try:
            # Fetch all Lab Requests with related patient data
            lab_reports = await sync_to_async(list)(
                LabReport.objects.select_related('lab_result','doctor').all()
            )
            
            # Prepare the response data
            response_data = [
                {
                    "id": lab_report.id,
                "lab_result": lab_report.lab_result.id,
                "doctor": f"{lab_report.doctor.first_name} {lab_report.doctor.last_name}",
                "report_data": lab_report.report_data,
                "generated_at": lab_report.generated_at.isoformat(),
                "shared_with_doctor": lab_report.shared_with_doctor,
                "report_file": lab_report.report_file.url if lab_report.report_file else None,
                }
                for lab_report in lab_reports
            ]
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            print("error is ", e)
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
        

