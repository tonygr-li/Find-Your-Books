# Generated by Django 3.1.6 on 2021-07-19 01:14

from django.db import migrations, models
import selling.models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0003_auto_20210716_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='expiry_date',
            field=models.DateTimeField(default=selling.models.two_months_hence),
        ),
    ]
