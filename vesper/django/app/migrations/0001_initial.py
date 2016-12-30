# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 18:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'vesper_algorithm',
            },
        ),
        migrations.CreateModel(
            name='AlgorithmVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('algorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='vesper.Algorithm')),
            ],
            options={
                'db_table': 'vesper_algorithm_version',
            },
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField(blank=True)),
                ('creation_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'vesper_annotation',
            },
        ),
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_num', models.IntegerField()),
                ('start_index', models.BigIntegerField(null=True)),
                ('length', models.BigIntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('creation_time', models.DateTimeField()),
                ('file_path', models.CharField(max_length=255, null=True, unique=True)),
            ],
            options={
                'db_table': 'vesper_clip',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('serial_number', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'vesper_device',
            },
        ),
        migrations.CreateModel(
            name='DeviceConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'vesper_device_connection',
            },
        ),
        migrations.CreateModel(
            name='DeviceInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='vesper.Device')),
            ],
            options={
                'db_table': 'vesper_device_input',
            },
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('type', models.CharField(max_length=255)),
                ('manufacturer', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'vesper_device_model',
            },
        ),
        migrations.CreateModel(
            name='DeviceModelInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_name', models.CharField(max_length=255)),
                ('channel_num', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inputs', to='vesper.DeviceModel')),
            ],
            options={
                'db_table': 'vesper_device_model_input',
            },
        ),
        migrations.CreateModel(
            name='DeviceModelOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_name', models.CharField(max_length=255)),
                ('channel_num', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='vesper.DeviceModel')),
            ],
            options={
                'db_table': 'vesper_device_model_output',
            },
        ),
        migrations.CreateModel(
            name='DeviceOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outputs', to='vesper.Device')),
                ('model_output', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_outputs', to='vesper.DeviceModelOutput')),
            ],
            options={
                'db_table': 'vesper_device_output',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command', models.TextField()),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=255)),
                ('creation_time', models.DateTimeField()),
                ('creating_job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='vesper.Job')),
                ('creating_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'vesper_job',
            },
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('settings', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('algorithm_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='processors', to='vesper.AlgorithmVersion')),
            ],
            options={
                'db_table': 'vesper_processor',
            },
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_channels', models.IntegerField()),
                ('length', models.BigIntegerField()),
                ('sample_rate', models.FloatField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('creation_time', models.DateTimeField()),
                ('creating_job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='vesper.Job')),
            ],
            options={
                'db_table': 'vesper_recording',
            },
        ),
        migrations.CreateModel(
            name='RecordingFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_num', models.IntegerField()),
                ('start_index', models.BigIntegerField()),
                ('length', models.BigIntegerField()),
                ('path', models.CharField(max_length=255, null=True, unique=True)),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='vesper.Recording')),
            ],
            options={
                'db_table': 'vesper_recording_file',
            },
        ),
        migrations.CreateModel(
            name='RecordingJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recording_jobs', to='vesper.Job')),
                ('recording', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recording_jobs', to='vesper.Recording')),
            ],
            options={
                'db_table': 'vesper_recording_job',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('elevation', models.FloatField(null=True)),
                ('time_zone', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'vesper_station',
            },
        ),
        migrations.CreateModel(
            name='StationDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='station_devices', to='vesper.Device')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='station_devices', to='vesper.Station')),
            ],
            options={
                'db_table': 'vesper_station_device',
            },
        ),
        migrations.AddField(
            model_name='station',
            name='devices',
            field=models.ManyToManyField(through='vesper.StationDevice', to='vesper.Device'),
        ),
        migrations.AddField(
            model_name='recording',
            name='station_recorder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='vesper.StationDevice'),
        ),
        migrations.AddField(
            model_name='job',
            name='processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='vesper.Processor'),
        ),
        migrations.AlterUniqueTogether(
            name='devicemodel',
            unique_together=set([('manufacturer', 'model')]),
        ),
        migrations.AddField(
            model_name='deviceinput',
            name='model_input',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_inputs', to='vesper.DeviceModelInput'),
        ),
        migrations.AddField(
            model_name='deviceconnection',
            name='input',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='vesper.DeviceInput'),
        ),
        migrations.AddField(
            model_name='deviceconnection',
            name='output',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections', to='vesper.DeviceOutput'),
        ),
        migrations.AddField(
            model_name='device',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='vesper.DeviceModel'),
        ),
        migrations.AddField(
            model_name='clip',
            name='creating_job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clips', to='vesper.Job'),
        ),
        migrations.AddField(
            model_name='clip',
            name='creating_processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clips', to='vesper.Processor'),
        ),
        migrations.AddField(
            model_name='clip',
            name='creating_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clips', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clip',
            name='recording',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clips', to='vesper.Recording'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='clip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='vesper.Clip'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='creating_job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='vesper.Job'),
        ),
        migrations.AddField(
            model_name='annotation',
            name='creating_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='stationdevice',
            unique_together=set([('station', 'device', 'start_time', 'end_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='recordingjob',
            unique_together=set([('recording', 'job')]),
        ),
        migrations.AlterUniqueTogether(
            name='recordingfile',
            unique_together=set([('recording', 'file_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='recording',
            unique_together=set([('station_recorder', 'start_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='deviceoutput',
            unique_together=set([('device', 'model_output')]),
        ),
        migrations.AlterUniqueTogether(
            name='devicemodeloutput',
            unique_together=set([('model', 'local_name'), ('model', 'channel_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='devicemodelinput',
            unique_together=set([('model', 'local_name'), ('model', 'channel_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='deviceinput',
            unique_together=set([('device', 'model_input')]),
        ),
        migrations.AlterUniqueTogether(
            name='deviceconnection',
            unique_together=set([('output', 'input', 'start_time', 'end_time')]),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('model', 'serial_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='clip',
            unique_together=set([('recording', 'channel_num', 'start_time', 'length', 'creating_processor')]),
        ),
        migrations.AlterUniqueTogether(
            name='annotation',
            unique_together=set([('clip', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='algorithmversion',
            unique_together=set([('algorithm', 'version')]),
        ),
    ]
