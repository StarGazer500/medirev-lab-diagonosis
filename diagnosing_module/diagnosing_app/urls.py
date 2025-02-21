from .template_views import *
from .api_views import *
from django.urls import path

urlpatterns = [

    #Template Views
    path('test/',AsyncTemplateView.as_view() , name='test'),

    #API Views
    path('create-patient/',CreatePatientView.as_view(),name="create-patient"),
    path('get-patient/<int:patient_id>/', GetPatientView.as_view(),name="get-patient"),
    path('create-doctor/',CreateDoctorView.as_view(),name="create-doctor"),
    path('get-doctor/<int:doctor_id>/', GetDoctorView.as_view(),name="get-doctor"),
    path('create-laborder-request',CreateLabOrderRequestView.as_view(),name="create-laborder-request"),
    path('get-laborder-request/<int:order_id>/',GetLabOrderRequestView.as_view(),name="get-laborder-request"),
    path('create-lab-results',CreateLabResultView.as_view(),name="create-lab-results"),
    path('get-lab-result/<int:lab_result_id>/',GetLabResultView.as_view(),name="get-lab-result"),
    path('create-lab-report', CreateLabReportView.as_view(),name="create-lab-report"),
    path('get-lab-reports/<int:lab_report_id>/',GetLabReportView.as_view(),name="get-lab-reports")
    
]