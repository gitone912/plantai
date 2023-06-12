# Generated by Django 4.2.1 on 2023-06-12 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("plants", "0003_plants_delete_plant"),
    ]

    operations = [
        migrations.CreateModel(
            name="Plant_details",
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
                    "common_names",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("edible_parts", models.TextField(blank=True, null=True)),
                ("gbif_id", models.IntegerField(blank=True, null=True)),
                (
                    "name_authority",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("propagation_methods", models.TextField(blank=True, null=True)),
                ("synonyms", models.TextField(blank=True, null=True)),
                ("taxonomy", models.TextField(blank=True, null=True)),
                ("url", models.URLField(blank=True, null=True)),
                ("wiki_description", models.TextField(blank=True, null=True)),
                ("wiki_image", models.URLField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Plants",
        ),
    ]
