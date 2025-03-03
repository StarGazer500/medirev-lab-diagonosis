from .template_views import *
from .api_views import *
from django.urls import path

urlpatterns = [

    #Template Views
    ##Patient Lab Request Template Views
    path('index/',LabRequestIndexTemaplateView.as_view() , name='index'),
    path('404/',LabRequest404TemaplateView.as_view() , name='404'),
    path('about/',LabRequestAboutTemaplateView.as_view() , name='about'),
    path('appointment/',LabRequestAppointmentTemaplateView.as_view() , name='appointment'),
    path('contact/',LabRequestContactTemaplateView.as_view() , name='contact'),
    path('feature/',LabRequestFeatureTemaplateView.as_view() , name='feature'),
    path('service/',LabRequestServiceTemaplateView.as_view() , name='service'),
    path('team/',LabRequestTeamTemaplateView.as_view() , name='team'),
    path('testimonial/',LabRequestTestimonialTemaplateView.as_view() , name='testimonial'),

    ##Lab Admin Templates
    path('add-appointment/',LabAdminAddAppointmentTemaplateView.as_view(), name='add-appointment'),
    path('add-department/',LabAdminAddDepartmentTemaplateView.as_view(), name='add-department'),
    path('add-doctor/',LabAdminAddDoctorTemaplateView.as_view(), name='add-doctor'),
    path('add-patient/',LabAdminAddPatientTemaplateView.as_view(), name='add-patient'),
    path('add-schedule/',LabAdminAddScheduleTemaplateView.as_view(), name='add-schedule'),
    path('add-lab-result/',LabAdminAddLabResultsTemaplateView.as_view(), name='add-lab-result'),
    path('add-lab-report/',LabAdminAddLabReportsTemaplateView.as_view(), name='add-lab-report'),
    path('appointments/',LabAdminAppointmentTemaplateView.as_view(), name='appointments'),
    path('departments/',LabAdminDepartmentTemaplateView.as_view(), name='departments'),
    path('doctors/',LabAdminDoctorsTemaplateView.as_view(), name='doctors'),
    path('edit-appointment/',LabAdminEditAppointmentTemaplateView.as_view(), name='edit-appointment'),
    path('edit-department/',LabAdminEditDepartmentTemaplateView.as_view(), name='edit-department'),
    path('edit-doctor/',LabAdminEditDoctorTemaplateView.as_view(), name='edit-doctor'),
    path('edit-patient/',LabAdminEditPatientTemaplateView.as_view(), name='edit-patient'),
    path('edit-profile/',LabAdminEditProfileTemaplateView.as_view(), name='edit-profile'),
    path('edit-schedule/',LabAdminEditScheduleTemaplateView.as_view(), name='edit-schedule'),
    path('edit-lab-result/',LabAdminEditLabResultTemaplateView.as_view(), name='edit-lab-result'),
    path('edit-lab-report/',LabAdminEditLabReportTemaplateView.as_view(), name='edit-lab-report'),
    path('index-2/',LabAdminIndex2TemaplateView.as_view(), name='index-2'),
    path('patients/',LabAdminPatientsTemaplateView.as_view(), name='patients'),
    path('profile/',LabAdminProfileTemaplateView.as_view(), name='profile'),
    path('schedule/',LabAdminScheduleTemaplateView.as_view(), name='schedule'),
    path('lab-results/',LabAdminResultTemaplateView.as_view(), name='lab-results'),
    path('lab-reports/',LabAdminReportTemaplateView.as_view(), name='lab-reports'),
    

    



    #API Views
    path('create-patient/',CreatePatientView.as_view(),name="create-patient"),
    path('get-patient/<int:patient_id>/', GetPatientView.as_view(),name="get-patient"),
    path('get-all-patient/', GetAllPatientView.as_view(),name='get-all-patient'),

    path('create-doctor/',CreateDoctorView.as_view(),name="create-doctor"),
    path('get-doctor/<int:doctor_id>/', GetDoctorView.as_view(),name="get-doctor"),

    path('create-laborder-request/',CreateLabOrderRequestView.as_view(),name="create-laborder-request"),
    path('get-laborder-request/<int:order_id>/',GetLabOrderRequestView.as_view(),name="get-laborder-request"),
    path('get-all-laborder-request/',GetAllLabOrderRequestView.as_view(),name='get-all-laborder-request'),

    path('create-lab-results/',CreateLabResultView.as_view(),name="create-lab-results"),
    path('get-lab-result/<int:lab_result_id>/',GetLabResultView.as_view(),name="get-lab-result"),

    path('create-lab-report', CreateLabReportView.as_view(),name="create-lab-report"),
    path('get-lab-reports/<int:lab_report_id>/',GetLabReportView.as_view(),name="get-lab-reports")
    
]