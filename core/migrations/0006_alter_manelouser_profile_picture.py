# Generated by Django 4.2 on 2024-02-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_manelouser_profile_picture_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manelouser',
            name='profile_picture',
            field=models.ImageField(default='default_user_icon.jpg', upload_to='users/images/<property object at 0x7fe484e11990>/'),
        ),
    ]