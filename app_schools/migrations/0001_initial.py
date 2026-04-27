from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("app_users", "0001_initial"),
        ("app_universities", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HasilPrediksi",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("siswa", models.ForeignKey(db_column="siswa_id", on_delete=django.db.models.deletion.CASCADE, related_name="hasil_prediksi", to="app_users.siswa")),
                ("prodi", models.ForeignKey(db_column="prodi_id", on_delete=django.db.models.deletion.CASCADE, related_name="hasil_prediksi", to="app_universities.prodi")),
                ("peluang_lulus", models.FloatField()),
                ("label_risiko", models.CharField(blank=True, max_length=50, null=True)),
                ("nilai_berbobot_saat_itu", models.FloatField(blank=True, null=True)),
                ("passing_grade_saat_itu", models.FloatField(blank=True, null=True)),
                ("rasio_keketatan_saat_itu", models.FloatField(blank=True, null=True)),
                ("rata_rata_saat_itu", models.FloatField(blank=True, null=True)),
                ("indeks_sekolah_saat_itu", models.FloatField(blank=True, null=True)),
                ("model_version", models.CharField(blank=True, max_length=50, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "hasil_prediksi", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="RekomendasiPTN",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("hasil_prediksi", models.ForeignKey(db_column="hasil_prediksi_id", on_delete=django.db.models.deletion.CASCADE, related_name="rekomendasi", to="app_predictions.hasilprediksi")),
                ("prodi", models.ForeignKey(db_column="prodi_id", on_delete=django.db.models.deletion.CASCADE, related_name="rekomendasi_ptn", to="app_universities.prodi")),
                ("peluang_estimasi", models.FloatField(blank=True, null=True)),
                ("passing_grade_ref", models.FloatField(blank=True, null=True)),
                ("rasio_keketatan_ref", models.FloatField(blank=True, null=True)),
                ("urutan", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "rekomendasi_ptn", "ordering": ["urutan"]},
        ),
        migrations.CreateModel(
            name="RoadmapNilai",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("siswa", models.ForeignKey(db_column="siswa_id", on_delete=django.db.models.deletion.CASCADE, related_name="roadmap_nilai", to="app_users.siswa")),
                ("prodi", models.ForeignKey(db_column="prodi_id", on_delete=django.db.models.deletion.CASCADE, related_name="roadmap_nilai", to="app_universities.prodi")),
                ("sem_terakhir_input", models.IntegerField()),
                ("target_sem3", models.FloatField(blank=True, null=True)),
                ("target_sem4", models.FloatField(blank=True, null=True)),
                ("target_sem5", models.FloatField(blank=True, null=True)),
                ("slope", models.FloatField(blank=True, null=True)),
                ("intercept", models.FloatField(blank=True, null=True)),
                ("passing_grade_target", models.FloatField(blank=True, null=True)),
                ("model_version", models.CharField(blank=True, max_length=50, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "roadmap_nilai", "ordering": ["-created_at"]},
        ),
    ]