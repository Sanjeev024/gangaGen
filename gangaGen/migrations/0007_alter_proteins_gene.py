# Generated by Django 5.0.4 on 2024-04-19 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gangaGen', '0006_proteins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proteins',
            name='gene',
            field=models.CharField(max_length=100, null=True),
        ),
    ]