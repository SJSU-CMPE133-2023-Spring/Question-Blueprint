# Generated by Django 4.1.7 on 2023-04-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_facebook_link_profile_linkedin_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
