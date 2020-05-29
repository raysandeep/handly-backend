# Generated by Django 3.0.5 on 2020-05-19 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_handwritinginputlogger_error_logger'),
    ]

    operations = [
        migrations.CreateModel(
            name='OutputFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='outputFiles/')),
                ('input_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.HandwritingInputLogger')),
            ],
        ),
    ]
