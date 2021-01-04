# Generated by Django 3.1.4 on 2021-01-04 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20210104_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='periodicity',
            field=models.CharField(choices=[('D', 'Daily'), ('2D', 'Bidaily'), ('3D', '3-day'), ('5D', '5-day'), ('W', 'Weekly'), ('2W', 'Biweekly'), ('M', 'Monthly')], max_length=55),
        ),
    ]