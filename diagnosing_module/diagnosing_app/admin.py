from django.contrib import admin
from .models import Patient, Doctor, LabOrderRequest, LabResult, LabReport

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'contact_number', 'email')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name', 'email', 'contact_number')
    ordering = ('last_name', 'first_name')

# Customize the Doctor Admin view
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty')
    search_fields = ('first_name', 'last_name', 'specialty')
    ordering = ('last_name', 'first_name')

class LabOrderRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_name', 'order_date', 'status')
    list_filter = ('status',)
    search_fields = ('test_name', 'patient__first_name', 'patient__last_name')

class LabResultAdmin(admin.ModelAdmin):
    list_display = ('lab_order', 'result', 'test_date')
    search_fields = ('lab_order__test_name',)

class LabReportAdmin(admin.ModelAdmin):
    list_display = ('lab_result', 'generated_at', 'shared_with_doctor')
    list_filter = ('shared_with_doctor',)
    search_fields = ('lab_result__lab_order__test_name',)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(LabOrderRequest, LabOrderRequestAdmin)
admin.site.register(LabResult, LabResultAdmin)
admin.site.register(LabReport, LabReportAdmin)
