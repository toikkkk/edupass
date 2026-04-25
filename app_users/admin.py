from django.contrib import admin
from .models import Siswa, RaporSiswa

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ["nama", "email", "kelas", "is_active"]
    search_fields = ["nama", "email"]

@admin.register(RaporSiswa)
class RaporSiswaAdmin(admin.ModelAdmin):
    list_display = ["siswa", "rata_rata", "semester_terakhir"]