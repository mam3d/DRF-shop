# Generated by Django 3.2.9 on 2021-11-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20211119_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='variation_choices',
            field=models.ManyToManyField(blank=True, to='shop.VariationChoice'),
        ),
    ]
