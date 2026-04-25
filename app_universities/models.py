from django.db import models


class PTN(models.Model):
    kode_resmi = models.CharField(max_length=20, unique=True)
    nama_ptn = models.CharField(max_length=255)
    akronim = models.CharField(max_length=50, blank=True, null=True)
    kategori = models.CharField(max_length=100, blank=True, null=True)
    provinsi = models.CharField(max_length=100, blank=True, null=True)
    kab_kota = models.CharField(max_length=120, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ptn"
        ordering = ["nama_ptn"]

    def __str__(self):
        return f"{self.nama_ptn} ({self.akronim})"


class Prodi(models.Model):
    ptn = models.ForeignKey(
        PTN,
        on_delete=models.CASCADE,
        db_column="ptn_id",
        related_name="prodi_set",
    )
    kode_prodi = models.CharField(max_length=20, unique=True)
    nama_prodi = models.CharField(max_length=255)
    jenjang = models.CharField(max_length=50, blank=True, null=True)
    kelompok = models.CharField(max_length=100, blank=True, null=True)
    portofolio = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "prodi"
        ordering = ["nama_prodi"]

    def __str__(self):
        return f"{self.nama_prodi} - {self.ptn.nama_ptn}"


class DayaTampung(models.Model):
    prodi = models.OneToOneField(
        Prodi,
        on_delete=models.CASCADE,
        db_column="prodi_id",
        related_name="daya_tampung",
    )
    daya_tampung_2026 = models.IntegerField(blank=True, null=True)
    peminat_2025 = models.IntegerField(blank=True, null=True)
    rasio_keketatan = models.FloatField(blank=True, null=True)
    sumber = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "daya_tampung"

    def __str__(self):
        return f"DT {self.prodi.nama_prodi}"


class PassingGrade(models.Model):
    prodi = models.ForeignKey(
        Prodi,
        on_delete=models.CASCADE,
        db_column="prodi_id",
        related_name="passing_grades",
    )
    nilai_rata_rata = models.FloatField()
    tahun = models.IntegerField()
    sumber = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "passing_grade"
        constraints = [
            models.UniqueConstraint(
                fields=["prodi_id", "tahun"],
                name="uniq_passing_grade_prodi_tahun",
            )
        ]

    def __str__(self):
        return f"PG {self.prodi.nama_prodi} ({self.tahun})"