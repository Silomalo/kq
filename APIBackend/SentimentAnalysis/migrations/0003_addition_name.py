# Generated by Django 4.1.13 on 2024-08-24 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SentimentAnalysis', '0002_addition'),
    ]

    operations = [
        migrations.AddField(
            model_name='addition',
            name='name',
            field=models.CharField(default='Joseph Silomalo', max_length=100),
        ),
    ]
