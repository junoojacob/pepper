# Generated by Django 4.1.2 on 2022-11-01 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='sale',
            field=models.IntegerField(blank=True),
        ),
    ]
