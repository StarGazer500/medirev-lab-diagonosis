from django.db import models
from django.utils import timezone

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"
    

class LabOrderRequest(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test_description = models.TextField(default="Initial data")
    order_date = models.DateTimeField(default=timezone.now)
    request_status = models.CharField(
        max_length=10, 
        choices=ORDER_STATUS_CHOICES, 
        default='PENDING'
    )
    requested_date = models.DateTimeField()
    
    def __str__(self):
        return f"Order #{self.id} - {self.test_description} for {self.patient}"

    # def is_completed(self):
    #     return self.status == 'COMPLETED'



class LabResult(models.Model):
    lab_order = models.OneToOneField(LabOrderRequest, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    result = models.TextField()
    test_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"Result for Order #{self.lab_order.id}"

 
class LabReport(models.Model):
    lab_result = models.OneToOneField(LabResult, on_delete=models.CASCADE)
    report_data = models.TextField()  
    generated_at = models.DateTimeField(auto_now_add=True)
    shared_with_doctor = models.BooleanField(default=False)
    def __str__(self):
        return f"Report for Order #{self.lab_result.lab_order.id}"

#  class Department():
#     department
