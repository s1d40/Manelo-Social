# Generated by Django 4.2 on 2024-02-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_manelouser_profile_picture_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manelouser',
            name='profile_picture',
            field=models.ImageField(default='static/core/users/default_user_icon.jpg', upload_to='static/core/users/images/<property object at 0x7f1d116cd800>/profile_picture.jpeg'),
        ),
    ]