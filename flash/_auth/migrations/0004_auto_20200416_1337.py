# Generated by Django 2.2 on 2020-04-16 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_auth', '0003_auto_20200414_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='date_joined',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
