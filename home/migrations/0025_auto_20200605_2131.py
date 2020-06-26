# Generated by Django 3.0.2 on 2020-06-05 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20200601_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinfo',
            name='Image',
            field=models.ImageField(blank=True, default='images/customer/profile/default/default-customer.jpg', null=True, upload_to='images/customer/profile/'),
        ),
        migrations.AlterField(
            model_name='vinfo',
            name='Image',
            field=models.ImageField(blank=True, default='images/vendor/profile/default/default-vendor.jpg', null=True, upload_to='images/vendor/profile/'),
        ),
    ]
