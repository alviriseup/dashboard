# Generated by Django 5.1 on 2024-11-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='banner_image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
