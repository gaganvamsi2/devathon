# Generated by Django 3.1.1 on 2020-10-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0002_auto_20201002_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='mess',
            name='mess_name',
            field=models.CharField(default='Ganga', max_length=4096),
        ),
    ]