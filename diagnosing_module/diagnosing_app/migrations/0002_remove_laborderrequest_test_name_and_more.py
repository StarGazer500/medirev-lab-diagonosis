# Generated by Django 5.1.6 on 2025-02-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosing_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laborderrequest',
            name='test_name',
        ),
        migrations.AddField(
            model_name='laborderrequest',
            name='test_description',
            field=models.TextField(default='Initial data'),
        ),
    ]
