# Generated by Django 3.2.9 on 2021-11-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_orderitem_variation_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variation',
            field=models.ManyToManyField(blank=True, to='shop.Variation'),
        ),
    ]
