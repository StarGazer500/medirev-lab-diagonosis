# Generated by Django 5.1.6 on 2025-02-25 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosing_app', '0002_remove_laborderrequest_test_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laborderrequest',
            old_name='status',
            new_name='request_status',
        ),
    ]
