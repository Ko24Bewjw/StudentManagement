# Generated by Django 2.0.5 on 2018-08-08 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StuAdmin1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='Teacher_Email',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='Teacher_Password',
            field=models.CharField(default='123456', max_length=20),
        ),
    ]
