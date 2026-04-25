from django.contrib import admin
from .models import HasilPrediksi, RekomendasiPTN, RoadmapNilai

@admin.register(HasilPrediksi)
class HasilPrediksiAdmin(admin.ModelAdmin):
    list_display = ["siswa", "prodi", "peluang_lulus", "label_risiko", "created_at"]
    list_filter = ["label_risiko"]

@admin.register(RekomendasiPTN)
class RekomendasiPTNAdmin(admin.ModelAdmin):
    list_display = ["hasil_prediksi", "prodi", "peluang_estimasi", "urutan"]

@admin.register(RoadmapNilai)
class RoadmapNilaiAdmin(admin.ModelAdmin):
    list_display = ["siswa", "prodi", "sem_terakhir_input", "created_at"]