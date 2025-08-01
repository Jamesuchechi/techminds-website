# Generated by Django 5.2.3 on 2025-07-04 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_rename_date_applied_application_submitted_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='attestation',
            field=models.FileField(blank=True, null=True, upload_to='attestation/'),
        ),
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
