from django.db import models


class Sekolah(models.Model):
    """Data 1000 sekolah terbaik nasional."""

    npsn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nama_sekolah = models.CharField(max_length=255)
    provinsi = models.CharField(max_length=100, blank=True, null=True)
    kab_kota = models.CharField(max_length=120, blank=True, null=True)
    jenis = models.CharField(max_length=30, blank=True, null=True)
    akreditasi = models.CharField(max_length=10, blank=True, null=True)
    indeks_sekolah = models.FloatField(blank=True, null=True)
    kuota_eligible = models.FloatField(blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sekolah"
        ordering = ["ranking"]

    def __str__(self):
        return f"{self.nama_sekolah} ({self.provinsi})"