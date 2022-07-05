# Generated by Django 3.2 on 2022-07-05 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(default='placeholder', max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='message',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
