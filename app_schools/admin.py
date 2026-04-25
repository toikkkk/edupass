from django.contrib import admin
from .models import Sekolah

@admin.register(Sekolah)
class SekolahAdmin(admin.ModelAdmin):
    list_display = ["nama_sekolah", "provinsi", "akreditasi", "ranking"]
    search_fields = ["nama_sekolah", "provinsi"]
    list_filter = ["akreditasi", "provinsi"]