# Generated by Django 2.1.7 on 2019-04-06 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s7uploads', '0010_auto_20190210_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='tagline',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
