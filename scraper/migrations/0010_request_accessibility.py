# Generated by Django 3.1.4 on 2021-01-04 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0009_auto_20210104_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='accessibility',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default='Private', max_length=55),
        ),
    ]
