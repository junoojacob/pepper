# Generated by Django 4.1.2 on 2022-11-02 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_coupon_discount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productoffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
                ('discount', models.IntegerField(default=0)),
            ],
        ),
    ]
