"""
IMPORT DATA KE MONGODB ATLAS - EduPass
Mengimport 4 dataset CSV ke collections MongoDB

CARA PAKAI:
  1. Pastikan file .env sudah ada di folder yang sama
  2. Install library:
     C:/Users/thori/AppData/Local/Programs/Python/Python311/python.exe -m pip install pymongo pandas python-dotenv
  3. Jalankan:
     C:/Users/thori/AppData/Local/Programs/Python/Python311/python.exe import_to_mongodb.py
"""

import os
import pandas as pd
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI    = os.getenv("MONGO_URI")
MONGO_DB     = os.getenv("MONGO_DB_NAME", "edupass")

# Path file CSV - sesuaikan dengan lokasi file Anda
CSV_FILES = {
    "dataset_final_ml":     "data/dataset_final_ml.csv",
    "passing_grade":        "data/passing_grade_clean.csv",
    "daya_tampung":         "data/daya_tampung_clean.csv",
    "indeks_sekolah":       "data/indeks_sekolah_clean.csv",
}

print("=" * 55)
print("  IMPORT DATA KE MONGODB ATLAS")
print("  Database: edupass")
print("=" * 55)


def connect_mongodb():
    print("\n  Menghubungkan ke MongoDB Atlas...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        client.server_info()
        print("  Koneksi berhasil!")
        return client
    except Exception as e:
        print("  GAGAL koneksi:", e)
        print("  Cek MONGO_URI di file .env")
        return None


def import_collection(db, collection_name, csv_path, indexes=None):
    print(f"\n  Importing {collection_name}...")
    print(f"  File: {csv_path}")

    if not os.path.exists(csv_path):
        print(f"  FILE TIDAK DITEMUKAN: {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    df = df.where(pd.notna(df), None)

    records = df.to_dict("records")

    col = db[collection_name]
    col.drop()

    result = col.insert_many(records)

    if indexes:
        for idx in indexes:
            col.create_index(idx)

    print(f"  Berhasil import {len(result.inserted_ids)} dokumen")
    return len(result.inserted_ids)


def main():
    client = connect_mongodb()
    if not client:
        return

    db    = client[MONGO_DB]
    total = 0

    # 1. Import dataset_final_ml (untuk training ML)
    total += import_collection(
        db, "dataset_ml",
        CSV_FILES["dataset_final_ml"],
        indexes=[
            [("target_ptn", ASCENDING)],
            [("target_prodi", ASCENDING)],
            [("akreditasi", ASCENDING)],
            [("target_lulus_snbp", ASCENDING)],
        ]
    )

    # 2. Import passing_grade
    total += import_collection(
        db, "passing_grade",
        CSV_FILES["passing_grade"],
        indexes=[
            [("nama_ptn", ASCENDING)],
            [("nama_prodi", ASCENDING)],
            [("nama_ptn", ASCENDING), ("nama_prodi", ASCENDING)],
        ]
    )

    # 3. Import daya_tampung
    total += import_collection(
        db, "daya_tampung",
        CSV_FILES["daya_tampung"],
        indexes=[
            [("nama_ptn", ASCENDING)],
            [("nama_prodi", ASCENDING)],
            [("kategori", ASCENDING)],
            [("rasio_keketatan", ASCENDING)],
        ]
    )

    # 4. Import indeks_sekolah
    total += import_collection(
        db, "indeks_sekolah",
        CSV_FILES["indeks_sekolah"],
        indexes=[
            [("nama_sekolah", ASCENDING)],
            [("ranking", ASCENDING)],
            [("akreditasi", ASCENDING)],
            [("provinsi", ASCENDING)],
        ]
    )

    # Verifikasi
    print("\n" + "=" * 55)
    print("  VERIFIKASI COLLECTIONS")
    print("=" * 55)
    for col_name in ["dataset_ml", "passing_grade", "daya_tampung", "indeks_sekolah"]:
        count = db[col_name].count_documents({})
        print(f"  {col_name:<20}: {count:>6} dokumen")

    print("\n" + "=" * 55)
    print(f"  SELESAI! Total: {total} dokumen diimport")
    print("=" * 55)
    print()
    print("  Cek data di: https://cloud.mongodb.com")
    print("  Database   : edupass")
    print("  Collections: dataset_ml, passing_grade,")
    print("               daya_tampung, indeks_sekolah")

    client.close()


if __name__ == "__main__":
    main()
