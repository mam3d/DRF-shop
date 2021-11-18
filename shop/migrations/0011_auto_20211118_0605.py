# Generated by Django 3.2.9 on 2021-11-18 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_variation_variationchoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='product',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='variation_choices',
            field=models.ManyToManyField(to='shop.VariationChoice'),
        ),
        migrations.AddField(
            model_name='product',
            name='variation',
            field=models.ManyToManyField(to='shop.Variation'),
        ),
    ]