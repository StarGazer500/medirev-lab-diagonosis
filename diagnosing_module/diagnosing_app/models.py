from django.db import models
from django.utils import timezone
from io import BytesIO
from django.core.files import File
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import requests


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
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
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
    result = models.TextField()
    test_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return f"Result for Order #{self.lab_order.id}"

 
class LabReport(models.Model):
    lab_result = models.OneToOneField(LabResult, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    report_data = models.TextField()
    report_file = models.FileField(upload_to='lab_reports/%Y/%m/%d/', null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    shared_with_doctor = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Report for Order #{self.lab_result.lab_order.id}"

    def generate_pdf_report(self):
        """Generate a nicely formatted PDF report with Miderev branding"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
        styles = getSampleStyleSheet()
        
        # Custom styles for Miderev branding
        styles.add(ParagraphStyle(name='CompanyTitle', fontSize=16, textColor=colors.white, backColor=colors.darkblue, alignment=1, spaceAfter=10))
        styles.add(ParagraphStyle(name='SectionHeader', fontSize=12, textColor=colors.black, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=5))
        styles.add(ParagraphStyle(name='Content', fontSize=10, textColor=colors.black, spaceAfter=5))

        story = []

        # Use a random placeholder image URL (e.g., from Lorem Picsum)
        placeholder_url = "https://picsum.photos/150/75"  # Random 150x75 image
        try:
            # Download the image
            response = requests.get(placeholder_url)
            response.raise_for_status()  # Check for HTTP errors
            image_data = BytesIO(response.content)
            logo = Image(image_data, width=1.5*inch, height=0.75*inch)
        except Exception as e:
            # Fallback in case of failure
            logo = Paragraph("Logo unavailable", styles['Content'])  # Fallback text if image fails

        # Header with Miderev branding (logo + company name)
        company_name = Paragraph("Miderev Lab Report", styles['CompanyTitle'])
        
        # Header table (logo on left, title on right)
        header_data = [[logo, company_name]]
        header_table = Table(header_data, colWidths=[2*inch, 4.5*inch])
        header_table.setStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.darkblue),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ])
        story.append(header_table)
        story.append(Spacer(1, 0.25*inch))

        # Doctor Information
        doctor_info = f"Prepared for: Dr. {self.doctor.first_name} {self.doctor.last_name}"
        story.append(Paragraph("Doctor Information", styles['SectionHeader']))
        story.append(Paragraph(doctor_info, styles['Content']))
        story.append(Spacer(1, 0.15*inch))

        # Lab Result Information
        lab_info = f"Lab Order #{self.lab_result.lab_order.id}"
        story.append(Paragraph("Lab Order Details", styles['SectionHeader']))
        story.append(Paragraph(lab_info, styles['Content']))
        story.append(Spacer(1, 0.15*inch))

        # Report Data
        story.append(Paragraph("Report Details", styles['SectionHeader']))
        story.append(Paragraph(self.report_data, styles['Content']))

        # Footer (generated date)
        footer_text = f"Generated on: {self.generated_at.strftime('%B %d, %Y %H:%M:%S')}"
        story.append(Spacer(1, 0.25*inch))
        story.append(Paragraph(footer_text, styles['Content']))

        # Build the PDF
        doc.build(story)

        # Save PDF to file field
        filename = f"lab_report_{self.id}.pdf"
        buffer.seek(0)
        if self.report_file:  # Delete old file if it exists
            self.report_file.delete(save=False)  # Remove the old file from storage
        self.report_file.save(filename, File(buffer), save=False)  # Save new file without triggering model save yet
        buffer.close()
        self.save()