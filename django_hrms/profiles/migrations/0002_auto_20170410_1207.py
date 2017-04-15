# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='attendance_standards',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('regular_sign_in_min', models.TimeField()),
                ('regular_sign_in_max', models.TimeField()),
                ('regular_sign_out_min', models.TimeField()),
                ('regular_sign_out_max', models.TimeField()),
                ('company', models.ForeignKey(to='profiles.company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='attendance_standard',
            name='company',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='attendance_standard',
        ),
        migrations.DeleteModel(
            name='attendance_standard',
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendance_standards',
            field=models.ForeignKey(to='profiles.attendance_standards', null=True),
            preserve_default=True,
        ),
    ]
