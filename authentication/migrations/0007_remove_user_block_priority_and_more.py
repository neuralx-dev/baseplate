# Generated by Django 4.2.3 on 2023-08-01 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0006_user_question_categories"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="block_priority",),
        migrations.RemoveField(model_name="user", name="question_categories",),
    ]