# Generated by Django 3.0.5 on 2020-05-19 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_outputfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handwritinginputlogger',
            name='input_file',
            field=models.FileField(upload_to='inputFiles/'),
        ),
        migrations.DeleteModel(
            name='InputFileLogger',
        ),
    ]
