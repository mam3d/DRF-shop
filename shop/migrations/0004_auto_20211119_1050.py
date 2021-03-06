# Generated by Django 3.2.9 on 2021-11-19 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_variationchoice_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='variation_choices',
            field=models.ManyToManyField(blank=True, null=True, to='shop.VariationChoice'),
        ),
        migrations.AlterField(
            model_name='variationchoice',
            name='variation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.variation'),
        ),
    ]
