# Generated by Django 4.1.5 on 2023-01-10 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_alter_blog_aritcle'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='eidtors_pick',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='visitors',
            field=models.IntegerField(default=0),
        ),
    ]