from django.db import models


class Siswa(models.Model):
    nama = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255)
    jurusan_sma = models.CharField(max_length=100, blank=True, null=True)
    kelas = models.CharField(max_length=20, blank=True, null=True)
    sekolah = models.ForeignKey(
        "app_schools.Sekolah",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="sekolah_id",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "siswa"

    def __str__(self):
        return f"{self.nama} ({self.email})"


class RaporSiswa(models.Model):
    siswa = models.OneToOneField(
        Siswa,
        on_delete=models.CASCADE,
        db_column="siswa_id",
        related_name="rapor",
    )
    nilai_sem1 = models.FloatField(blank=True, null=True)
    nilai_sem2 = models.FloatField(blank=True, null=True)
    nilai_sem3 = models.FloatField(blank=True, null=True)
    nilai_sem4 = models.FloatField(blank=True, null=True)
    nilai_sem5 = models.FloatField(blank=True, null=True)
    rata_rata = models.FloatField(blank=True, null=True)
    nilai_berbobot = models.FloatField(blank=True, null=True)
    semester_terakhir = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rapor_siswa"

    def __str__(self):
        return f"Rapor {self.siswa.nama}"