# Generated by Django 5.1.6 on 2025-03-05 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosing_app', '0003_rename_status_laborderrequest_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laborderrequest',
            name='patient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='diagnosing_app.patient'),
        ),
    ]
