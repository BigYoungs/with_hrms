# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_condition_status', models.CharField(default=b'in_attend', max_length=10, choices=[(b'in_attend', b'\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8a\xe7\x8f\xad'), (b'late', b'\xe8\xbf\x9f\xe5\x88\xb0')])),
                ('out_condition_status', models.CharField(default=b'out_attend', max_length=10, choices=[(b'out_attend', b'\xe6\xad\xa3\xe5\xb8\xb8\xe4\xb8\x8b\xe7\x8f\xad'), (b'earlyout', b'\xe6\x97\xa9\xe9\x80\x80')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='attendance_data',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendance_day', models.DateField()),
                ('sign_in', models.TimeField()),
                ('sign_out', models.TimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['attendance_day'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='attendance_standard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regular_sign_in_min', models.TimeField()),
                ('regular_sign_in_max', models.TimeField()),
                ('regular_sign_out_min', models.TimeField()),
                ('regular_sign_out_max', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(unique=True, max_length=30)),
                ('company_loca', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department_name', models.CharField(max_length=30)),
                ('department_comment', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='duties',
            fields=[
                ('duty_id', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('duty_name', models.CharField(max_length=30)),
                ('department', models.ForeignKey(to='profiles.department', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'name')),
                ('sex', models.CharField(max_length=1, choices=[(b'F', b'Female'), (b'M', b'Male')])),
                ('birth', models.DateField(help_text=b'\xe8\xbe\x93\xe5\x85\xa5\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba YYYY-MM-DD', null=True, verbose_name=b'birth')),
                ('birth_place', models.CharField(max_length=50, verbose_name=b'birth_place')),
                ('nation', models.CharField(max_length=20, verbose_name=b'nation')),
                ('identification_num', models.CharField(max_length=18, verbose_name=b'identification_num')),
                ('political', models.CharField(max_length=50, null=True)),
                ('graduation_school', models.CharField(max_length=30, null=True)),
                ('graduation_date', models.DateField(help_text=b'\xe8\xbe\x93\xe5\x85\xa5\xe6\xa0\xbc\xe5\xbc\x8f\xe4\xb8\xba YYYY-MM-DD', null=True)),
                ('education', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=75, null=True)),
                ('status', models.CharField(max_length=1, choices=[(b'Z', b'\xe5\x9c\xa8\xe8\x81\x8c'), (b'L', b'\xe7\xa6\xbb\xe8\x81\x8c'), (b'O', b'\xe5\x81\x9c\xe8\x81\x8c'), (b'T', b'\xe9\x80\x80\xe4\xbc\x91')])),
                ('company', models.ForeignKey(to='profiles.company', null=True)),
                ('department', models.ForeignKey(to='profiles.department', null=True)),
                ('duty', models.ForeignKey(to='profiles.duties', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='salary_cs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salary_should_sent_time', models.CharField(max_length=30)),
                ('salary_total', models.DecimalField(max_digits=11, decimal_places=2)),
                ('salary_actual', models.DecimalField(max_digits=11, decimal_places=2)),
                ('sent_salary_status', models.BooleanField(default=False, verbose_name=b'\xe5\xb7\xa5\xe8\xb5\x84\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe5\x8f\x91\xe6\x94\xbe\xef\xbc\x9f')),
                ('attendance', models.ForeignKey(to='profiles.attendance', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='salary_standard',
            fields=[
                ('salary_lev_id', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('salary_lev_name', models.CharField(max_length=10)),
                ('basic_salary', models.DecimalField(max_digits=11, decimal_places=2)),
                ('subsidy', models.DecimalField(max_digits=11, decimal_places=2)),
                ('housing_fund', models.DecimalField(max_digits=11, decimal_places=2)),
                ('social_security', models.DecimalField(max_digits=11, decimal_places=2)),
                ('bonus', models.DecimalField(max_digits=11, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='salary_cs',
            name='salary_standard',
            field=models.ForeignKey(to='profiles.salary_standard', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='salary_cs',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='duties',
            name='salary_lev_id',
            field=models.ForeignKey(to='profiles.salary_standard', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance_standard',
            name='company',
            field=models.ForeignKey(to='profiles.company'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='attendance_data',
            unique_together=set([('user', 'attendance_day')]),
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendance_data',
            field=models.ForeignKey(to='profiles.attendance_data', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendance_standard',
            field=models.ForeignKey(to='profiles.attendance_standard', null=True),
            preserve_default=True,
        ),
    ]
