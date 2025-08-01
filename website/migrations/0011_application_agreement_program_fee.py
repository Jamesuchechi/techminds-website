# Generated by Django 5.2.3 on 2025-07-10 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_remove_contactmessage_program_contact_office_hours_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='agreement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='program',
            name='fee',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True),
        ),
    ]
