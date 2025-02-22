

# Create your views here.
from django.views.generic import TemplateView
from asgiref.sync import sync_to_async

class LabRequestIndexTemaplateView(TemplateView):
    template_name = "lab_request/index.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequest404TemaplateView(TemplateView):
    template_name = "lab_request/404.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequestAboutTemaplateView(TemplateView):
    template_name = "lab_request/about.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
    
class LabRequestAppointmentTemaplateView(TemplateView):
    template_name = "lab_request/appoinment.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context


class LabRequestContactTemaplateView(TemplateView):
    template_name = "lab_request/contact.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequestFeatureTemaplateView(TemplateView):
    template_name = "lab_request/feature.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequestServiceTemaplateView(TemplateView):
    template_name = "lab_request/service.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequestTeamTemaplateView(TemplateView):
    template_name = "lab_request/team.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabRequestTestimonialTemaplateView(TemplateView):
    template_name = "lab_request/testimonial.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    



class LabAdminAddAppointmentTemaplateView(TemplateView):
    template_name = "lab_admin/add-appointment.html"
   
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddDepartmentTemaplateView(TemplateView):
    template_name = "lab_admin/add-department.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddDoctorTemaplateView(TemplateView):
    template_name = "lab_admin/add-doctor.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddPatientTemaplateView(TemplateView):
    template_name = "lab_admin/add-patient.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddScheduleTemaplateView(TemplateView):
    template_name = "lab_admin/add-schedule.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAppointmentTemaplateView(TemplateView):
    template_name = "lab_admin/appointments.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    

class LabAdminDepartmentTemaplateView(TemplateView):
    template_name = "lab_admin/departments.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminDoctorsTemaplateView(TemplateView):
    template_name = "lab_admin/doctors.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditAppointmentTemaplateView(TemplateView):
    template_name = "lab_admin/edit-appointment.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditDepartmentTemaplateView(TemplateView):
    template_name = "lab_admin/edit-department.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    

class LabAdminEditDoctorTemaplateView(TemplateView):
    template_name = "lab_admin/edit-doctor.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditPatientTemaplateView(TemplateView):
    template_name = "lab_admin/edit-patient.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditProfileTemaplateView(TemplateView):
    template_name = "lab_admin/edit-profile.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditScheduleTemaplateView(TemplateView):
    template_name = "lab_admin/edit-schedule.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminIndex2TemaplateView(TemplateView):
    template_name = "lab_admin/index-2.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminPatientsTemaplateView(TemplateView):
    template_name = "lab_admin/patients.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminProfileTemaplateView(TemplateView):
    template_name = "lab_admin/profile.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    

class LabAdminScheduleTemaplateView(TemplateView):
    template_name = "lab_admin/schedule.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddLabResultsTemaplateView(TemplateView):
    template_name = "lab_admin/add-lab-result.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminAddLabReportsTemaplateView(TemplateView):
    template_name = "lab_admin/add-lab-report.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditLabResultTemaplateView(TemplateView):
    template_name = "lab_admin/edit-lab-result.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminEditLabReportTemaplateView(TemplateView):
    template_name = "lab_admin/edit-lab-report.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminResultTemaplateView(TemplateView):
    template_name = "lab_admin/lab-results.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context
    
class LabAdminReportTemaplateView(TemplateView):
    template_name = "lab_admin/lab-reports.html"
    async def get(self, request, *args, **kwargs):
        context = await self.get_context_data(**kwargs)
        return self.render_to_response(context)

    async def get_context_data(self, **kwargs):
        # Convert the synchronous get_context_data to async
        context = await sync_to_async(super().get_context_data)(**kwargs)
        # Add any additional async context here
        return context