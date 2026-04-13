# EduPass - Sistem Analisis Prediktif SNBP

## Setup Project

### 1. Clone repository
git clone https://github.com/toikkkk/edupass.git
cd edupass

### 2. Install dependencies
pip install -r requirements.txt

### 3. Setup .env
Buat file .env di root folder, isi dengan:
MONGO_URI=<minta ke Toriq>
MONGO_DB_NAME=edupass
SECRET_KEY=edupass-secret-key-2026
DEBUG=True

### 4. Test koneksi
python -c "from dotenv import load_dotenv; ..."

### 5. Jalankan server
python manage.py runserver