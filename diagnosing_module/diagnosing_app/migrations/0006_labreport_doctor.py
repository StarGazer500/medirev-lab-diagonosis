# Generated by Django 5.1.6 on 2025-03-05 13:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosing_app', '0005_remove_labresult_doctor_labreport_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='labreport',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='diagnosing_app.doctor'),
        ),
    ]
