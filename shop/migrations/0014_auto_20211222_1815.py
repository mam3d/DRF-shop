# Generated by Django 3.2.9 on 2021-12-22 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_alter_orderitem_variation_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variationchoice',
            name='variation',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='variation_choices',
        ),
        migrations.RemoveField(
            model_name='product',
            name='variation',
        ),
        migrations.DeleteModel(
            name='Variation',
        ),
        migrations.DeleteModel(
            name='VariationChoice',
        ),
    ]
