from .template_views import *
from .api_views import *
from django.urls import path

urlpatterns = [

    #Template Views
    path('test/',AsyncTemplateView.as_view() , name='test'),

    #API Views
    path('create-patient/',CreatePatientView.as_view(),name="create-patient"),
    path('get-patient/', GetPatientView.as_view(),name="get-patient"),
    path('create-laborder-request',CreateLabOrderRequestView.as_view(),name="create-laborder-request"),
    path('get-laborder-request',GetLabOrderRequestView.as_view(),name="get-laborder-request"),
    path('create-lab-results',CreateLabResultView.as_view(),name="create-lab-results"),
    path('get-lab-request/',GetLabResultView.as_view(),name="get-lab-request"),
    path('create-lab-report', CreateLabReportView.as_view(),name="create-lab-report"),
    path('get-lab-reports',GetLabReportView.as_view(),name="get-lab-reports")
    
]