# Generated by Django 3.1.4 on 2021-01-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_processingstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text',
            name='sentiment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
