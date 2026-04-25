from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True
    dependencies = [
        ("app_schools", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Siswa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nama", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("jurusan_sma", models.CharField(blank=True, max_length=100, null=True)),
                ("kelas", models.CharField(blank=True, max_length=20, null=True)),
                ("sekolah", models.ForeignKey(blank=True, db_column="sekolah_id", null=True, on_delete=django.db.models.deletion.SET_NULL, to="app_schools.sekolah")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "siswa"},
        ),
        migrations.CreateModel(
            name="RaporSiswa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("siswa", models.OneToOneField(db_column="siswa_id", on_delete=django.db.models.deletion.CASCADE, related_name="rapor", to="app_users.siswa")),
                ("nilai_sem1", models.FloatField(blank=True, null=True)),
                ("nilai_sem2", models.FloatField(blank=True, null=True)),
                ("nilai_sem3", models.FloatField(blank=True, null=True)),
                ("nilai_sem4", models.FloatField(blank=True, null=True)),
                ("nilai_sem5", models.FloatField(blank=True, null=True)),
                ("rata_rata", models.FloatField(blank=True, null=True)),
                ("nilai_berbobot", models.FloatField(blank=True, null=True)),
                ("semester_terakhir", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "rapor_siswa"},
        ),
    ]