# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0002_auto_20170410_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendances',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_condition_status', models.CharField(default=b'in_attend', max_length=10, choices=[(b'in_attend', b'\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8a\xe7\x8f\xad'), (b'late', b'\xe8\xbf\x9f\xe5\x88\xb0')])),
                ('out_condition_status', models.CharField(default=b'out_attend', max_length=10, choices=[(b'out_attend', b'\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8b\xe7\x8f\xad'), (b'earlyout', b'\xe6\x97\xa9\xe9\x80\x80')])),
                ('attendance_day', models.ForeignKey(to='profiles.attendance_data')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='attendance_data',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='attendance_standards',
        ),
        migrations.AlterField(
            model_name='attendance_standards',
            name='regular_sign_in_max',
            field=models.TimeField(help_text=b'\xe6\x97\xa9\xe4\xb8\x8a\xe8\xbf\x9f\xe5\x88\xb0\xe6\x97\xb6\xe9\x97\xb4\xe7\xbb\x88\xe7\x82\xb9   ---- **\xe9\x99\x90\xe5\x88\xb6\xe7\xad\xbe\xe5\x88\xb0\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\xae\xb5 \xe5\x8d\xb3min_max'),
        ),
        migrations.AlterField(
            model_name='attendance_standards',
            name='regular_sign_in_min',
            field=models.TimeField(help_text=b'\xe6\x97\xa9\xe4\xb8\x8a\xe8\xbf\x9f\xe5\x88\xb0\xe6\x97\xb6\xe9\x97\xb4\xe8\xb5\xb7\xe7\x82\xb9   ---- **\xe7\xad\xbe\xe5\x88\xb0\xe6\x9c\x80\xe6\x97\xa9\xe6\x97\xb6\xe9\x97\xb4\xe6\xaf\x94\xe8\xbf\x99\xe9\xa1\xb9\xe6\x97\xa9\xef\xbc\x8c\xe4\xb8\xba\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8a\xe7\x8f\xad'),
        ),
        migrations.AlterField(
            model_name='attendance_standards',
            name='regular_sign_out_max',
            field=models.TimeField(help_text=b'\xe4\xb8\x8b\xe5\x8d\x88\xe6\x97\xa9\xe9\x80\x80\xe6\x97\xb6\xe9\x97\xb4\xe7\xbb\x88\xe7\x82\xb9  ----**\xe7\xad\xbe\xe9\x80\x80\xe6\x9c\x80\xe6\x99\x9a\xe6\x97\xb6\xe9\x97\xb4\xe6\xaf\x94\xe8\xbf\x99\xe9\xa1\xb9\xe6\x99\x9a\xef\xbc\x8c\xe4\xb8\xba\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8b\xe7\x8f\xad'),
        ),
        migrations.AlterField(
            model_name='attendance_standards',
            name='regular_sign_out_min',
            field=models.TimeField(help_text=b'\xe4\xb8\x8b\xe5\x8d\x88\xe6\x97\xa9\xe9\x80\x80\xe6\x97\xb6\xe9\x97\xb4\xe8\xb5\xb7\xe7\x82\xb9  ---- **\xe9\x99\x90\xe5\x88\xb6\xe7\xad\xbe\xe9\x80\x80\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe6\xae\xb5 \xe5\x8d\xb3min_max'),
        ),
        migrations.AlterField(
            model_name='salary_cs',
            name='attendance',
            field=models.ForeignKey(to='profiles.attendances', null=True),
        ),
        migrations.DeleteModel(
            name='attendance',
        ),
    ]
