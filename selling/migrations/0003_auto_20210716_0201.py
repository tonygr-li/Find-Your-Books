# Generated by Django 3.1.6 on 2021-07-16 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0002_auto_20210715_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='phone_contact',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]