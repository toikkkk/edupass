import pandas as pd
import numpy as np
import os
from datetime import datetime

np.random.seed(42)

print("=" * 60)
print("  PREPROCESSING EDUPASS")
print("  Mempersiapkan dataset untuk training ML")
print("=" * 60)


# LOAD SEMUA DATA

print("\n[1/7] Loading semua dataset...")

df_rapor   = pd.read_csv("dataset_dummy_rapor_snbp.csv")
df_sekolah = pd.read_csv("dataset_indeks_sekolah_top1000_4.csv")
df_nilai   = pd.read_csv("nilai_eligible_snbp.csv")
df_daya    = pd.read_csv("daya_tampung_snbp.csv")

print("  Rapor siswa    :", df_rapor.shape)
print("  Indeks sekolah :", df_sekolah.shape)
print("  Nilai eligible :", df_nilai.shape)
print("  Daya tampung   :", df_daya.shape)


# STEP 1: BERSIHKAN NILAI ELIGIBLE

print("\n[2/7] Membersihkan nilai eligible (passing grade)...")

df_nilai_clean = df_nilai[["nama_ptn","akronim","nama_prodi","jenjang","nilai_rata_rata"]].copy()
df_nilai_clean = df_nilai_clean.dropna(subset=["nilai_rata_rata"])
df_nilai_clean = df_nilai_clean[df_nilai_clean["nilai_rata_rata"] > 0]
df_nilai_clean["nama_prodi"] = df_nilai_clean["nama_prodi"].str.strip().str.upper()
df_nilai_clean["nama_ptn"]   = df_nilai_clean["nama_ptn"].str.strip().str.upper()
df_nilai_clean = df_nilai_clean.drop_duplicates(subset=["nama_ptn","nama_prodi"])
df_nilai_clean = df_nilai_clean.reset_index(drop=True)

print("  Passing grade bersih :", df_nilai_clean.shape)
print("  Range nilai          :", df_nilai_clean["nilai_rata_rata"].min(), "-", df_nilai_clean["nilai_rata_rata"].max())


# STEP 2: BERSIHKAN DAYA TAMPUNG

print("\n[3/7] Membersihkan daya tampung...")

df_daya_clean = df_daya[[
    "nama_ptn","kode_resmi","kategori","kode_prodi",
    "nama_prodi","jenjang","daya_tampung_2026",
    "peminat_2025","portofolio","rasio_keketatan"
]].copy()
df_daya_clean["nama_prodi"] = df_daya_clean["nama_prodi"].str.strip().str.upper()
df_daya_clean["nama_ptn"]   = df_daya_clean["nama_ptn"].str.strip().str.upper()
df_daya_clean = df_daya_clean.dropna(subset=["daya_tampung_2026"])
df_daya_clean = df_daya_clean.drop_duplicates(subset=["nama_ptn","nama_prodi"])
df_daya_clean = df_daya_clean.reset_index(drop=True)

print("  Daya tampung bersih :", df_daya_clean.shape)
print("  PTN unik            :", df_daya_clean["nama_ptn"].nunique())


# STEP 3: SIAPKAN INDEKS SEKOLAH

print("\n[4/7] Menyiapkan indeks sekolah...")

df_sekolah_clean = df_sekolah.copy()
df_sekolah_clean.columns = ["ranking","npsn","nama_sekolah","provinsi","kab_kota","jenis"]

# Akreditasi berdasarkan ranking nasional
def get_akreditasi(r):
    if r <= 100:  return "A"
    elif r <= 400: return "B"
    else:          return "C"

df_sekolah_clean["akreditasi"] = df_sekolah_clean["ranking"].apply(get_akreditasi)

# Indeks sekolah sebagai MULTIPLIER (skala 0.85 - 1.0)
# Ranking 1 = 1.0, Ranking 1000 = 0.85
# Sesuai konsep makalah: Nilai Berbobot = rata_rata x (indeks/100)
# Indeks dalam skala 85-100
df_sekolah_clean["indeks_sekolah"] = (
    100.0 - (df_sekolah_clean["ranking"] - 1) / (1000 - 1) * 15.0
).round(2)

# Kuota eligible berdasarkan akreditasi
kuota_map = {"A": 0.40, "B": 0.25, "C": 0.05}
df_sekolah_clean["kuota_eligible"] = df_sekolah_clean["akreditasi"].map(kuota_map)

print("  Sekolah bersih       :", df_sekolah_clean.shape)
print("  Distribusi akreditasi:", df_sekolah_clean["akreditasi"].value_counts().to_dict())
print("  Range indeks         :", df_sekolah_clean["indeks_sekolah"].min(), "-", df_sekolah_clean["indeks_sekolah"].max())


# STEP 4: PERBAIKI DATASET RAPOR SISWA

print("\n[5/7] Memperbaiki dataset rapor siswa...")

df_ml = df_rapor[["nama","jurusan_sma","nilai_sem1","nilai_sem2",
                   "nilai_sem3","nilai_sem4"]].copy()

# 4a. Tambah nilai_sem5
def generate_sem5(row):
    vals  = [row["nilai_sem1"],row["nilai_sem2"],row["nilai_sem3"],row["nilai_sem4"]]
    tren  = (vals[-1] - vals[0]) / 3
    base  = vals[-1] + tren * 0.5
    noise = np.random.normal(0, 0.8)
    return round(min(max(base + noise, 60.0), 100.0), 1)

df_ml["nilai_sem5"] = df_ml.apply(generate_sem5, axis=1)

# 4b. Hitung rata_rata dari sem1-sem5
df_ml["rata_rata"] = df_ml[["nilai_sem1","nilai_sem2","nilai_sem3","nilai_sem4","nilai_sem5"]].mean(axis=1).round(2)

# 4c. Assign sekolah secara random
sekolah_sample = df_sekolah_clean.sample(n=len(df_ml), replace=True).reset_index(drop=True)
df_ml["nama_sekolah"]   = sekolah_sample["nama_sekolah"].values
df_ml["ranking"]        = sekolah_sample["ranking"].values
df_ml["akreditasi"]     = sekolah_sample["akreditasi"].values
df_ml["indeks_sekolah"] = sekolah_sample["indeks_sekolah"].values
df_ml["kuota_eligible"] = sekolah_sample["kuota_eligible"].values
df_ml["provinsi"]       = sekolah_sample["provinsi"].values

# 4d. Hitung nilai_berbobot sesuai rumus makalah:
# Nilai Berbobot = rata_rata x (indeks_sekolah / 100)
df_ml["nilai_berbobot"] = (df_ml["rata_rata"] * (df_ml["indeks_sekolah"] / 100)).round(2)

# 4e. Assign target_ptn & target_prodi secara random
ptn_prodi = df_daya_clean[["nama_ptn","nama_prodi","jenjang"]].drop_duplicates().reset_index(drop=True)
idx_rand  = np.random.randint(0, len(ptn_prodi), size=len(df_ml))
df_ml["target_ptn"]     = ptn_prodi.loc[idx_rand, "nama_ptn"].values
df_ml["target_prodi"]   = ptn_prodi.loc[idx_rand, "nama_prodi"].values
df_ml["target_jenjang"] = ptn_prodi.loc[idx_rand, "jenjang"].values

# 4f. Join passing grade
df_ml = df_ml.merge(
    df_nilai_clean[["nama_ptn","nama_prodi","nilai_rata_rata"]].rename(columns={
        "nama_ptn":      "target_ptn",
        "nama_prodi":    "target_prodi",
        "nilai_rata_rata":"passing_grade"
    }),
    on=["target_ptn","target_prodi"],
    how="left"
)

# 4g. Join daya tampung
df_ml = df_ml.merge(
    df_daya_clean[["nama_ptn","nama_prodi","daya_tampung_2026","peminat_2025","rasio_keketatan"]].rename(columns={
        "nama_ptn":   "target_ptn",
        "nama_prodi": "target_prodi",
    }),
    on=["target_ptn","target_prodi"],
    how="left"
)

# Isi nilai kosong dengan median
df_ml["passing_grade"]    = df_ml["passing_grade"].fillna(df_nilai_clean["nilai_rata_rata"].median())
df_ml["daya_tampung_2026"] = df_ml["daya_tampung_2026"].fillna(df_daya_clean["daya_tampung_2026"].median())
df_ml["peminat_2025"]     = df_ml["peminat_2025"].fillna(df_daya_clean["peminat_2025"].median())
df_ml["rasio_keketatan"]  = df_ml["rasio_keketatan"].fillna(df_daya_clean["rasio_keketatan"].median())

print("  Shape setelah enrichment:", df_ml.shape)
print("  Sample nilai_berbobot   :", df_ml["nilai_berbobot"].head(3).tolist())
print("  Sample passing_grade    :", df_ml["passing_grade"].head(3).tolist())


# STEP 5: HITUNG LABEL REALISTIS (target 25-35% lulus)

print("\n[6/7] Menghitung label target_lulus_snbp yang realistis...")

# Logika SNBP yang sesuai makalah:
# 1. Hitung nilai_berbobot = rata_rata x (indeks_sekolah/100)
# 2. Bandingkan dengan passing_grade prodi target
# 3. Pertimbangkan rasio keketatan prodi
# 4. Acceptance rate nasional SNBP ~20-22%

def hitung_label_realistis(row):
    nb = row["nilai_berbobot"]
    pg = row["passing_grade"]
    rk = row["rasio_keketatan"]

    # Hitung skor kompetitif: seberapa dekat nilai berbobot dengan passing grade
    # nilai_berbobot range ~75-98, passing_grade range ~60-95
    # Normalisasi: skor = (nilai_berbobot - passing_grade) / std_passing_grade
    selisih = nb - pg

    # Faktor keketatan: semakin kecil rasio, semakin susah
    if pd.notna(rk):
        if rk < 0.05:    faktor = -3.0   # sangat ketat
        elif rk < 0.10:  faktor = -1.5   # ketat
        elif rk < 0.20:  faktor = 0.0    # sedang
        elif rk < 0.40:  faktor = 1.0    # longgar
        else:            faktor = 2.0    # sangat longgar
    else:
        faktor = 0.0

    skor_total = selisih + faktor

    # Konversi ke probabilitas lulus (target ~25% overall)
    prob = 1 / (1 + np.exp(-0.3 * skor_total))

    return int(np.random.random() < prob)

df_ml["target_lulus_snbp"] = df_ml.apply(hitung_label_realistis, axis=1)

label_dist    = df_ml["target_lulus_snbp"].value_counts().to_dict()
lulus_pct     = round(label_dist.get(1,0) / len(df_ml) * 100, 1)
tdk_lulus_pct = round(label_dist.get(0,0) / len(df_ml) * 100, 1)

print("  Distribusi label:")
print(f"    Lulus (1)      : {label_dist.get(1,0)} siswa ({lulus_pct}%)")
print(f"    Tidak lulus (0): {label_dist.get(0,0)} siswa ({tdk_lulus_pct}%)")


# STEP 6: FINALISASI KOLOM DAN SIMPAN

print("\n[7/7] Finalisasi dan simpan...")

kolom_final = [
    "nama", "jurusan_sma",
    "nilai_sem1","nilai_sem2","nilai_sem3","nilai_sem4","nilai_sem5",
    "rata_rata",
    "nama_sekolah","ranking","akreditasi","indeks_sekolah","kuota_eligible","provinsi",
    "nilai_berbobot",
    "target_ptn","target_prodi","target_jenjang",
    "passing_grade","daya_tampung_2026","peminat_2025","rasio_keketatan",
    "target_lulus_snbp",
]

kolom_ada = [c for c in kolom_final if c in df_ml.columns]
df_final  = df_ml[kolom_ada].copy()

print("  Kolom final   :", len(kolom_ada))
print("  Shape final   :", df_final.shape)
print("  Nilai kosong  :", df_final.isna().sum().sum())

# Simpan semua file output
df_final.to_csv("dataset_final_ml.csv", index=False, encoding="utf-8-sig")
df_nilai_clean.to_csv("passing_grade_clean.csv", index=False, encoding="utf-8-sig")
df_daya_clean.to_csv("daya_tampung_clean.csv", index=False, encoding="utf-8-sig")
df_sekolah_clean.to_csv("indeks_sekolah_clean.csv", index=False, encoding="utf-8-sig")

# Laporan
report = f"""LAPORAN PREPROCESSING EDUPASS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*55}

INPUT DATASET:
  Rapor siswa    : {df_rapor.shape[0]:>5} baris | {df_rapor.shape[1]} kolom
  Indeks sekolah : {df_sekolah.shape[0]:>5} baris | {df_sekolah.shape[1]} kolom
  Nilai eligible : {df_nilai.shape[0]:>5} baris | {df_nilai.shape[1]} kolom
  Daya tampung   : {df_daya.shape[0]:>5} baris | {df_daya.shape[1]} kolom

OUTPUT DATASET:
  dataset_final_ml.csv     : {df_final.shape[0]:>5} baris | {df_final.shape[1]} kolom
  passing_grade_clean.csv  : {df_nilai_clean.shape[0]:>5} baris | {df_nilai_clean.shape[1]} kolom
  daya_tampung_clean.csv   : {df_daya_clean.shape[0]:>5} baris | {df_daya_clean.shape[1]} kolom
  indeks_sekolah_clean.csv : {df_sekolah_clean.shape[0]:>5} baris | {df_sekolah_clean.shape[1]} kolom

PERUBAHAN PADA RAPOR SISWA:
  + nilai_sem5        : ditambahkan (estimasi dari tren sem1-sem4)
  + rata_rata         : dihitung ulang dari sem1-sem5
  + nama_sekolah      : ditambahkan (dari indeks sekolah)
  + ranking           : peringkat nasional sekolah
  + akreditasi        : A/B/C (berdasarkan ranking)
  + indeks_sekolah    : multiplier 85-100 (sesuai makalah)
  + kuota_eligible    : persentase siswa yang boleh daftar
  + provinsi          : lokasi sekolah
  + nilai_berbobot    : rata_rata x (indeks_sekolah/100)
  + target_ptn        : PTN yang dipilih siswa
  + target_prodi      : Prodi yang dipilih
  + passing_grade     : nilai minimal lolos prodi tersebut
  + daya_tampung_2026 : kuota kursi prodi
  + peminat_2025      : jumlah peminat tahun lalu
  + rasio_keketatan   : daya_tampung / peminat
  + target_lulus_snbp : label realistis berdasarkan logika SNBP

DISTRIBUSI LABEL:
  Lulus (1)      : {label_dist.get(1,0):>4} siswa ({lulus_pct}%)
  Tidak Lulus (0): {label_dist.get(0,0):>4} siswa ({tdk_lulus_pct}%)

KOLOM DATASET FINAL (untuk training ML):
{chr(10).join(['  ' + str(i+1).zfill(2) + '. ' + c for i, c in enumerate(df_final.columns)])}

KETERANGAN KOLOM:
  Fitur utama Random Forest  : nilai_berbobot, passing_grade,
                               rasio_keketatan, akreditasi, indeks_sekolah
  Fitur Linear Regression    : nilai_sem1-sem5, rata_rata, indeks_sekolah
  Label                      : target_lulus_snbp (0=tidak lulus, 1=lulus)
"""

with open("preprocessing_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print()
print("=" * 60)
print("  PREPROCESSING SELESAI!")
print("=" * 60)
print()
print("  File output:")
print("  1. dataset_final_ml.csv      <- UTAMA: untuk training ML")
print("  2. passing_grade_clean.csv   <- referensi passing grade")
print("  3. daya_tampung_clean.csv    <- referensi daya tampung")
print("  4. indeks_sekolah_clean.csv  <- referensi indeks sekolah")
print("  5. preprocessing_report.txt  <- laporan lengkap")
print()
print("  Preview 5 baris pertama dataset_final_ml.csv:")
print("  " + "-"*55)
cols_show = ["rata_rata","indeks_sekolah","nilai_berbobot","passing_grade","rasio_keketatan","target_lulus_snbp"]
cols_show = [c for c in cols_show if c in df_final.columns]
print(df_final[cols_show].head(5).to_string(index=False))
print()
print("  Langkah selanjutnya: Training Model ML")
print("  -> Random Forest  : prediksi peluang lolos SNBP")
print("  -> Linear Regression : roadmap target nilai per semester")

