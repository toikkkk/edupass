from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sekolah",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("npsn", models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ("nama_sekolah", models.CharField(max_length=255)),
                ("provinsi", models.CharField(blank=True, max_length=100, null=True)),
                ("kab_kota", models.CharField(blank=True, max_length=120, null=True)),
                ("jenis", models.CharField(blank=True, max_length=30, null=True)),
                ("akreditasi", models.CharField(blank=True, max_length=10, null=True)),
                ("indeks_sekolah", models.FloatField(blank=True, null=True)),
                ("kuota_eligible", models.FloatField(blank=True, null=True)),
                ("ranking", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "sekolah", "ordering": ["ranking"]},
        ),
    ]