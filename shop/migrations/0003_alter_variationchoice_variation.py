# Generated by Django 3.2.9 on 2021-11-19 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variationchoice',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.variation'),
        ),
    ]