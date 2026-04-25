import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Koneksi PostgreSQL
conn = psycopg2.connect(
    dbname   = os.getenv("DB_NAME", "postgres"),
    user     = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD", "w4u7pyQV77lnuiHX"),
    host     = os.getenv("DB_HOST"),
    port     = os.getenv("DB_PORT", "5432"),
    sslmode  = "require"
)
cur = conn.cursor()

DATA_DIR = "data"

print("=" * 55)
print("  IMPORT DATA CSV KE POSTGRESQL - EduPass")
print("=" * 55)


# ─────────────────────────────────────────────
# 1. IMPORT SEKOLAH
# ─────────────────────────────────────────────

def import_sekolah():
    print("\n[1/3] Import indeks_sekolah_clean.csv -> tabel sekolah...")
    df = pd.read_csv(os.path.join(DATA_DIR, "indeks_sekolah_clean.csv"))
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")

    cur.execute("DELETE FROM sekolah")

    insert_sql = """
        INSERT INTO sekolah (npsn, nama_sekolah, provinsi, kab_kota, jenis,
                             akreditasi, indeks_sekolah, kuota_eligible, ranking)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (npsn) DO NOTHING
    """

    rows = []
    for _, row in df.iterrows():
        npsn = str(row.get("npsn", "")).strip()
        if not npsn or npsn == "nan":
            npsn = f"NPSN{int(row.get('ranking', 0))}"

        rows.append((
            npsn,
            str(row["nama_sekolah"]).strip(),
            str(row.get("provinsi","")).strip() or None,
            str(row.get("kab_kota","")).strip() or None,
            str(row.get("jenis","SMA")).strip(),
            str(row.get("akreditasi","B")).strip(),
            float(row.get("indeks_sekolah", 90)),
            float(row.get("kuota_eligible", 0.25)),
            int(row.get("ranking", 500)),
        ))

    cur.executemany(insert_sql, rows)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM sekolah")
    print(f"  Berhasil: {cur.fetchone()[0]} sekolah")


# ─────────────────────────────────────────────
# 2. IMPORT PTN + PRODI + DAYA TAMPUNG
# ─────────────────────────────────────────────

def import_daya_tampung():
    print("\n[2/3] Import daya_tampung_clean.csv -> tabel ptn, prodi, daya_tampung...")
    df = pd.read_csv(os.path.join(DATA_DIR, "daya_tampung_clean.csv"))
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")
    df["nama_ptn"]   = df["nama_ptn"].str.strip().str.upper()
    df["nama_prodi"] = df["nama_prodi"].str.strip().str.upper()

    cur.execute("DELETE FROM daya_tampung")
    cur.execute("DELETE FROM prodi")
    cur.execute("DELETE FROM ptn")
    conn.commit()

    # Import PTN (unik per kode_resmi)
    ptn_unik = df.drop_duplicates("kode_resmi")[["nama_ptn","kode_resmi","kategori"]]
    ptn_sql  = """
        INSERT INTO ptn (kode_resmi, nama_ptn, kategori)
        VALUES (%s, %s, %s)
        ON CONFLICT (kode_resmi) DO NOTHING
    """
    ptn_rows = []
    for _, row in ptn_unik.iterrows():
        ptn_rows.append((
            str(row["kode_resmi"]).strip(),
            str(row["nama_ptn"]).strip(),
            str(row.get("kategori","PTN Akademik")).strip(),
        ))
    cur.executemany(ptn_sql, ptn_rows)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM ptn")
    print(f"  PTN: {cur.fetchone()[0]}")

    # Buat mapping kode_resmi -> ptn.id
    cur.execute("SELECT id, kode_resmi FROM ptn")
    ptn_map = {row[1]: row[0] for row in cur.fetchall()}

    # Import Prodi
    prodi_sql = """
        INSERT INTO prodi (ptn_id, kode_prodi, nama_prodi, jenjang)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (kode_prodi) DO NOTHING
        RETURNING id, kode_prodi
    """
    prodi_map = {}
    for _, row in df.iterrows():
        kode_ptn   = str(row["kode_resmi"]).strip()
        ptn_id     = ptn_map.get(kode_ptn)
        if not ptn_id:
            continue

        kode_prodi = str(row.get("kode_prodi","")).strip()
        if not kode_prodi or kode_prodi == "nan":
            continue

        nama_prodi = str(row["nama_prodi"]).strip()
        jenjang    = str(row.get("jenjang","Sarjana")).strip()

        try:
            cur.execute("""
                INSERT INTO prodi (ptn_id, kode_prodi, nama_prodi, jenjang)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (kode_prodi) DO UPDATE SET nama_prodi=EXCLUDED.nama_prodi
                RETURNING id
            """, (ptn_id, kode_prodi, nama_prodi, jenjang))
            result = cur.fetchone()
            if result:
                prodi_map[(kode_ptn, nama_prodi)] = result[0]
        except Exception:
            conn.rollback()

    conn.commit()
    cur.execute("SELECT COUNT(*) FROM prodi")
    print(f"  Prodi: {cur.fetchone()[0]}")

    # Import Daya Tampung
    dt_sql = """
        INSERT INTO daya_tampung (prodi_id, daya_tampung_2026, peminat_2025, rasio_keketatan, sumber)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (prodi_id) DO NOTHING
    """
    dt_rows = []
    for _, row in df.iterrows():
        kode_ptn   = str(row["kode_resmi"]).strip()
        nama_prodi = str(row["nama_prodi"]).strip()
        prodi_id   = prodi_map.get((kode_ptn, nama_prodi))
        if not prodi_id:
            continue

        dt_val = row.get("daya_tampung_2026")
        pm_val = row.get("peminat_2025")
        rasio  = row.get("rasio_keketatan")

        dt_rows.append((
            prodi_id,
            int(dt_val) if pd.notna(dt_val) else None,
            int(pm_val) if pd.notna(pm_val) else None,
            float(rasio) if pd.notna(rasio) else None,
            "sidata-ptn.snpmb.id",
        ))

    cur.executemany(dt_sql, dt_rows)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM daya_tampung")
    print(f"  Daya tampung: {cur.fetchone()[0]}")


# ─────────────────────────────────────────────
# 3. IMPORT PASSING GRADE
# ─────────────────────────────────────────────

def import_passing_grade():
    print("\n[3/3] Import passing_grade_clean.csv -> tabel passing_grade...")
    df = pd.read_csv(os.path.join(DATA_DIR, "passing_grade_clean.csv"))
    df.columns = df.columns.str.strip().str.lstrip("\ufeff")
    df["nama_ptn"]   = df["nama_ptn"].str.strip().str.upper()
    df["nama_prodi"] = df["nama_prodi"].str.strip().str.upper()

    cur.execute("DELETE FROM passing_grade")
    conn.commit()

    # Buat mapping akronim -> ptn.id
    cur.execute("SELECT id, akronim, nama_ptn FROM ptn")
    ptn_rows    = cur.fetchall()
    akronim_map = {}
    nama_map    = {}
    for pid, akronim, nama_ptn in ptn_rows:
        if akronim:
            akronim_map[akronim.upper()] = pid
        nama_map[nama_ptn.upper()] = pid

    # Buat mapping (ptn_id, nama_prodi) -> prodi.id
    cur.execute("SELECT id, ptn_id, nama_prodi FROM prodi")
    prodi_map = {(row[1], row[2].upper()): row[0] for row in cur.fetchall()}

    pg_sql = """
        INSERT INTO passing_grade (prodi_id, nilai_rata_rata, tahun, sumber)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (prodi_id, tahun) DO NOTHING
    """

    pg_rows = []
    skip    = 0
    for _, row in df.iterrows():
        akronim_csv  = str(row.get("akronim","")).strip().upper()
        nama_ptn_csv = str(row["nama_ptn"]).strip().upper()
        nama_prodi   = str(row["nama_prodi"]).strip().upper()
        nilai        = row.get("nilai_rata_rata")

        if pd.isna(nilai):
            skip += 1
            continue

        ptn_id = akronim_map.get(akronim_csv) or nama_map.get(nama_ptn_csv)
        if not ptn_id:
            skip += 1
            continue

        prodi_id = prodi_map.get((ptn_id, nama_prodi))
        if not prodi_id:
            skip += 1
            continue

        pg_rows.append((prodi_id, float(nilai), 2026, "haipintar.com"))

    cur.executemany(pg_sql, pg_rows)
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM passing_grade")
    print(f"  Passing grade: {cur.fetchone()[0]} (skip: {skip})")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    try:
        import_sekolah()
        import_daya_tampung()
        import_passing_grade()

        print("\n" + "="*55)
        print("  SELESAI! Ringkasan data di PostgreSQL:")
        print("="*55)

        for tabel in ["sekolah","ptn","prodi","daya_tampung","passing_grade"]:
            cur.execute(f"SELECT COUNT(*) FROM {tabel}")
            print(f"  {tabel:<20}: {cur.fetchone()[0]:>6} baris")

        print()
        print("  Data sudah siap di PostgreSQL!")
        print("  Cek di pgAdmin -> database edupass -> Tables")

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
