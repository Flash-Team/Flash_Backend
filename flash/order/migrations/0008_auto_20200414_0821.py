# Generated by Django 2.2 on 2020-04-14 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20200413_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='filial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='organization.Filial'),
        ),
    ]