# Generated by Django 5.1.1 on 2024-10-06 14:12

import django.db.models.deletion
import django.utils.timezone
import portfolio.fields
import portfolio.utils
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MediaFile",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                (
                    "file_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=5
                    ),
                ),
                ("file", models.FileField(upload_to=portfolio.utils.content_file_name)),
                ("is_public", models.BooleanField(default=True)),
                ("thumbnail", models.URLField(blank=True, max_length=500, null=True)),
            ],
            options={
                "ordering": ["-update_date"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MediaPosition",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255)),
                ("layout", models.JSONField()),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
            ],
            options={
                "ordering": ["-update_date"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="HistoricalMediaFile",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "ip_address",
                    models.GenericIPAddressField(null=True, verbose_name="IP address"),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(blank=True, editable=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "file_type",
                    models.CharField(
                        choices=[("image", "Image"), ("video", "Video")], max_length=5
                    ),
                ),
                ("file", models.CharField(max_length=100)),
                ("is_public", models.BooleanField(default=True)),
                ("thumbnail", models.URLField(blank=True, max_length=500, null=True)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical media file",
                "verbose_name_plural": "historical media files",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalMediaPosition",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "ip_address",
                    models.GenericIPAddressField(null=True, verbose_name="IP address"),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(blank=True, editable=False)),
                ("name", models.CharField(blank=True, max_length=255)),
                ("layout", models.JSONField()),
                ("slug", models.SlugField(blank=True, max_length=255)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical media position",
                "verbose_name_plural": "historical media positions",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalProcessedMediaFile",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "ip_address",
                    models.GenericIPAddressField(null=True, verbose_name="IP address"),
                ),
                (
                    "uuid",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(blank=True, editable=False)),
                ("processed_file", models.CharField(max_length=100)),
                ("resolution", portfolio.fields.ResolutionField(blank=True, null=True)),
                ("quality", models.IntegerField(default=75)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processing", "Processing"),
                            ("ready", "Ready"),
                            ("failed", "Failed"),
                        ],
                        default="processing",
                        max_length=20,
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "media_file",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="portfolio.mediafile",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical processed media file",
                "verbose_name_plural": "historical processed media files",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="ProcessedMediaFile",
            fields=[
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "create_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "processed_file",
                    models.FileField(upload_to=portfolio.utils.content_file_name),
                ),
                ("resolution", portfolio.fields.ResolutionField(blank=True, null=True)),
                ("quality", models.IntegerField(default=75)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("processing", "Processing"),
                            ("ready", "Ready"),
                            ("failed", "Failed"),
                        ],
                        default="processing",
                        max_length=20,
                    ),
                ),
                (
                    "media_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="portfolio.mediafile",
                    ),
                ),
            ],
            options={
                "ordering": ["-update_date"],
                "abstract": False,
            },
        ),
    ]
