# Generated by Django 3.0.6 on 2020-05-29 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HandwritingInputLogger',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('input_file', models.FileField(upload_to='inputFiles/')),
                ('status', models.BooleanField(default=False)),
                ('error_status', models.BooleanField(default=False)),
                ('error_logger', models.CharField(default='No error', max_length=100)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Collections')),
            ],
        ),
        migrations.CreateModel(
            name='OutputFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('input_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.HandwritingInputLogger')),
            ],
        ),
    ]
