import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("energi", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TopikForum",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("judul", models.CharField(max_length=200)),
                ("isi", models.TextField()),
                ("kategori", models.CharField(
                    choices=[("Energi", "Energi"), ("Laporan", "Laporan"), ("Umum", "Umum")],
                    default="Umum",
                    max_length=50,
                )),
                ("dibuat_pada", models.DateTimeField(auto_now_add=True)),
                ("diperbarui_pada", models.DateTimeField(auto_now=True)),
                ("pinned", models.BooleanField(default=False)),
                ("penulis", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="topik_forum",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"ordering": ["-pinned", "-dibuat_pada"]},
        ),
        migrations.CreateModel(
            name="BalasanForum",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("isi", models.TextField()),
                ("dibuat_pada", models.DateTimeField(auto_now_add=True)),
                ("topik", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="balasan",
                    to="energi.topikforum",
                )),
                ("penulis", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="balasan_forum",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"ordering": ["dibuat_pada"]},
        ),
    ]