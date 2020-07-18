# Generated by Django 2.2.12 on 2020-07-18 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('s7uploads', '0011_upload_tagline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='tagline',
        ),
        migrations.AddField(
            model_name='upload',
            name='total_downloads',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upload',
            name='version_downloads',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('uploads', models.ManyToManyField(related_name='tags', to='s7uploads.Upload')),
            ],
        ),
    ]