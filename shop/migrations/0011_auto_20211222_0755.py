# Generated by Django 3.2.9 on 2021-12-22 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20211120_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='idpay_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='idpay_track_id',
        ),
    ]