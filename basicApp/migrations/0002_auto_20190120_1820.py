# Generated by Django 2.1.5 on 2019-01-20 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]