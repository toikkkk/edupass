from django.db import models


class HasilPrediksi(models.Model):
    siswa = models.ForeignKey(
        "app_users.Siswa",
        on_delete=models.CASCADE,
        db_column="siswa_id",
        related_name="hasil_prediksi",
    )
    prodi = models.ForeignKey(
        "app_universities.Prodi",
        on_delete=models.CASCADE,
        db_column="prodi_id",
        related_name="hasil_prediksi",
    )
    peluang_lulus = models.FloatField()
    label_risiko = models.CharField(max_length=50, blank=True, null=True)
    nilai_berbobot_saat_itu = models.FloatField(blank=True, null=True)
    passing_grade_saat_itu = models.FloatField(blank=True, null=True)
    rasio_keketatan_saat_itu = models.FloatField(blank=True, null=True)
    rata_rata_saat_itu = models.FloatField(blank=True, null=True)
    indeks_sekolah_saat_itu = models.FloatField(blank=True, null=True)
    model_version = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hasil_prediksi"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.siswa.nama} -> {self.prodi.nama_prodi} ({self.peluang_lulus:.1%})"


class RekomendasiPTN(models.Model):
    hasil_prediksi = models.ForeignKey(
        HasilPrediksi,
        on_delete=models.CASCADE,
        db_column="hasil_prediksi_id",
        related_name="rekomendasi",
    )
    prodi = models.ForeignKey(
        "app_universities.Prodi",
        on_delete=models.CASCADE,
        db_column="prodi_id",
        related_name="rekomendasi_ptn",
    )
    peluang_estimasi = models.FloatField(blank=True, null=True)
    passing_grade_ref = models.FloatField(blank=True, null=True)
    rasio_keketatan_ref = models.FloatField(blank=True, null=True)
    urutan = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rekomendasi_ptn"
        ordering = ["urutan"]

    def __str__(self):
        return f"Rekomendasi #{self.urutan} untuk prediksi {self.hasil_prediksi_id}"


class RoadmapNilai(models.Model):
    siswa = models.ForeignKey(
        "app_users.Siswa",
        on_delete=models.CASCADE,
        db_column="siswa_id",
        related_name="roadmap_nilai",
    )
    prodi = models.ForeignKey(
        "app_universities.Prodi",
        on_delete=models.CASCADE,
        db_column="prodi_id",
        related_name="roadmap_nilai",
    )
    sem_terakhir_input = models.IntegerField()
    target_sem3 = models.FloatField(blank=True, null=True)
    target_sem4 = models.FloatField(blank=True, null=True)
    target_sem5 = models.FloatField(blank=True, null=True)
    slope = models.FloatField(blank=True, null=True)
    intercept = models.FloatField(blank=True, null=True)
    passing_grade_target = models.FloatField(blank=True, null=True)
    model_version = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "roadmap_nilai"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Roadmap {self.siswa.nama} -> {self.prodi.nama_prodi}"