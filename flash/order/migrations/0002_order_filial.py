# Generated by Django 2.2 on 2020-03-30 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='filial',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='organization.Filial'),
        ),
    ]
