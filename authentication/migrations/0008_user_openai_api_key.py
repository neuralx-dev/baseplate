# Generated by Django 4.2.3 on 2023-09-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0007_remove_user_block_priority_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="openai_api_key",
            field=models.CharField(default="", max_length=255),
        ),
    ]
