# Generated by Django 4.2.3 on 2023-08-21 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Tool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=150)),
                ("about", models.CharField(default="", max_length=500)),
                ("desc", models.TextField(default="", max_length=10500)),
                ("banner", models.FileField(upload_to="images/banners/")),
                ("logo", models.FileField(default="", upload_to="images/logos/")),
                ("link", models.CharField(default="", max_length=150)),
                ("tags", models.CharField(default="", max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="ToolLike",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tool",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="toolbot.tool",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
