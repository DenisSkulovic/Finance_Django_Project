# Generated by Django 3.1.4 on 2021-01-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20210103_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='sentiment',
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('Unprocessed', 'Unprocessed'), ('Processing', 'Processing'), ('Processed', 'Processed')], default='Unprocessed', max_length=55),
        ),
        migrations.AddField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('Unprocessed', 'Unprocessed'), ('Processing', 'Processing'), ('Processed', 'Processed')], default='Unprocessed', max_length=55),
        ),
        migrations.AddField(
            model_name='text',
            name='sentiment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='text',
            name='status',
            field=models.CharField(choices=[('Unprocessed', 'Unprocessed'), ('Processing', 'Processing'), ('Processed', 'Processed')], default='Unprocessed', max_length=55),
        ),
    ]
