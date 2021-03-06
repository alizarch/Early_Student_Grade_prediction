# Generated by Django 3.1.7 on 2021-05-18 08:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esgpapp', '0005_auto_20210511_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv_content',
            name='grades',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='csv_content',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 13, 6, 2, 657669)),
        ),
        migrations.AlterField(
            model_name='csv_content',
            name='student_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='student_id'),
        ),
        migrations.AlterField(
            model_name='csv_content',
            name='student_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='student_name'),
        ),
        migrations.AlterField(
            model_name='csv_content',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 13, 6, 2, 657669)),
        ),
        migrations.AlterField(
            model_name='users',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 13, 6, 2, 655670)),
        ),
        migrations.AlterField(
            model_name='users',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 13, 6, 2, 655670)),
        ),
    ]
