# Generated by Django 2.2 on 2020-04-24 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import flash.organization.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20200416_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='organizations_logo', validators=[flash.organization.validators.validate_file_size, flash.organization.validators.validate_extension]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]
