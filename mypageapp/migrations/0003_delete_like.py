# Generated by Django 4.2.5 on 2023-11-28 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypageapp', '0002_like_remove_review_food_remove_review_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]