from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PTN",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kode_resmi", models.CharField(max_length=20, unique=True)),
                ("nama_ptn", models.CharField(max_length=255)),
                ("akronim", models.CharField(blank=True, max_length=50, null=True)),
                ("kategori", models.CharField(blank=True, max_length=100, null=True)),
                ("provinsi", models.CharField(blank=True, max_length=100, null=True)),
                ("kab_kota", models.CharField(blank=True, max_length=120, null=True)),
                ("website", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "ptn", "ordering": ["nama_ptn"]},
        ),
        migrations.CreateModel(
            name="Prodi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ptn", models.ForeignKey(db_column="ptn_id", on_delete=django.db.models.deletion.CASCADE, related_name="prodi_set", to="app_universities.ptn")),
                ("kode_prodi", models.CharField(max_length=20, unique=True)),
                ("nama_prodi", models.CharField(max_length=255)),
                ("jenjang", models.CharField(blank=True, max_length=50, null=True)),
                ("kelompok", models.CharField(blank=True, max_length=100, null=True)),
                ("portofolio", models.BooleanField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "prodi", "ordering": ["nama_prodi"]},
        ),
        migrations.CreateModel(
            name="DayaTampung",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prodi", models.OneToOneField(db_column="prodi_id", on_delete=django.db.models.deletion.CASCADE, related_name="daya_tampung", to="app_universities.prodi")),
                ("daya_tampung_2026", models.IntegerField(blank=True, null=True)),
                ("peminat_2025", models.IntegerField(blank=True, null=True)),
                ("rasio_keketatan", models.FloatField(blank=True, null=True)),
                ("sumber", models.CharField(blank=True, max_length=255, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "daya_tampung"},
        ),
        migrations.CreateModel(
            name="PassingGrade",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("prodi", models.ForeignKey(db_column="prodi_id", on_delete=django.db.models.deletion.CASCADE, related_name="passing_grades", to="app_universities.prodi")),
                ("nilai_rata_rata", models.FloatField()),
                ("tahun", models.IntegerField()),
                ("sumber", models.CharField(blank=True, max_length=255, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "passing_grade"},
        ),
        migrations.AddConstraint(
            model_name="passinggrade",
            constraint=models.UniqueConstraint(
                fields=["prodi_id", "tahun"],
                name="uniq_passing_grade_prodi_tahun",
            ),
        ),
    ]