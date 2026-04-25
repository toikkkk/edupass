from django.contrib import admin
from .models import PTN, Prodi, DayaTampung, PassingGrade

@admin.register(PTN)
class PTNAdmin(admin.ModelAdmin):
    list_display = ["nama_ptn", "akronim", "kategori", "provinsi"]
    search_fields = ["nama_ptn", "akronim"]

@admin.register(Prodi)
class ProdiAdmin(admin.ModelAdmin):
    list_display = ["nama_prodi", "ptn", "jenjang"]
    search_fields = ["nama_prodi"]
    list_filter = ["jenjang"]

@admin.register(DayaTampung)
class DayaTampungAdmin(admin.ModelAdmin):
    list_display = ["prodi", "daya_tampung_2026", "peminat_2025", "rasio_keketatan"]

@admin.register(PassingGrade)
class PassingGradeAdmin(admin.ModelAdmin):
    list_display = ["prodi", "nilai_rata_rata", "tahun"]