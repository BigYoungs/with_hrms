# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170411_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_standards',
            name='missed_time_total_max',
            field=models.IntegerField(default=3, help_text=b'\xe6\x97\xa9\xe4\xb8\x8a\xe8\xbf\x9f\xe5\x88\xb0\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe5\x8a\xa0\xe4\xb8\x8a\xe4\xb8\x8b\xe5\x8d\x88\xe6\x97\xa9\xe9\x80\x80\xe6\x97\xb6\xe9\x97\xb4\xe7\x9a\x84\xe6\x80\xbb\xe5\x92\x8c\xe3\x80\x82\xe8\xb6\x85\xe8\xbf\x87\xe8\xbf\x99\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe5\x88\x99\xe7\xae\x97\xe6\x97\xb7\xe5\xb7\xa5'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendances',
            name='not_attend',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
