# Generated by Django 3.0.2 on 2020-04-19 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200420_0025'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vinfo',
            old_name='Dp',
            new_name='Image',
        ),
        migrations.AlterField(
            model_name='cinfo',
            name='Username',
            field=models.TextField(),
        ),
    ]
