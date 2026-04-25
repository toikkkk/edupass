# EduPass - Sistem Analisis Prediktif SNBP

## Perubahan database
Project ini sudah dikonfigurasi ulang untuk menggunakan **PostgreSQL** melalui **Django ORM**.
MongoDB tidak lagi diperlukan untuk penyimpanan utama aplikasi.

## Setup Project

### 1. Clone repository
```bash
git clone https://github.com/toikkkk/edupass.git
cd edupass
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment
Salin file contoh environment:
```bash
cp .env.example .env
```

Lalu sesuaikan nilai berikut sesuai PostgreSQL Anda:
```env
DB_NAME=edupass
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### 4. Buat database PostgreSQL
Contoh di psql:
```sql
CREATE DATABASE edupass;
```

### 5. Jalankan migrasi
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Import data CSV ke PostgreSQL
```bash
python import_to_postgres.py
```

### 7. Jalankan server
```bash
python manage.py runserver
```

## Struktur data yang dipindahkan
- `dataset_final_ml.csv` -> `student_prediction_datasets`
- `passing_grade_clean.csv` -> `passing_grades`
- `daya_tampung_clean.csv` -> `capacities`
- `indeks_sekolah_clean.csv` -> `school_indexes`

## Catatan
- File `import_to_mongodb.py` adalah versi lama dan tidak dipakai lagi.
- Bila ingin menghapus dependensi MongoDB sepenuhnya, file helper MongoDB lama dapat dihapus.
