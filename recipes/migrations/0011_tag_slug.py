# Generated by Django 3.2.3 on 2021-06-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_recipe_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
