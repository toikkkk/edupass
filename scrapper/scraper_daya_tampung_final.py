import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime

BASE_URL = "https://sidatagrun-public-1076756628210.asia-southeast2.run.app/ptn_sn.php"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/146.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-id;q=0.9,id;q=0.8",
    "Referer": "https://sidatagrun-public-1076756628210.asia-southeast2.run.app/ptn_sn.php",
}

KATEGORI = [
    ("PTN Akademik", None),
    ("PTN Vokasi",   "-2"),
    ("PT KIN",       "-3"),
]

DELAY_MIN = 1.0
DELAY_MAX = 2.5


def fetch(params=None):
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except Exception as e:
        print("    [ERROR]", e)
    return None


# ─────────────────────────────────────────────
# TAHAP 1: Ambil semua kode PTN dari halaman daftar
# Link Lihat Prodi: href="?ptn=111" -> kode = 111
# ─────────────────────────────────────────────

def get_ptn_list(nama_kat, param_kat):
    print("  Kategori:", nama_kat)

    params = {"ptn": param_kat} if param_kat else {}
    soup   = fetch(params)
    if not soup:
        return []

    ptn_list = []
    table    = soup.find("table")
    if not table:
        return []

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        # Kolom terakhir: tombol Lihat Prodi dengan href="?ptn=111"
        lihat_lnk = cells[-1].find("a", href=True)
        if not lihat_lnk:
            continue
        href     = lihat_lnk["href"]
        kode_ptn = href.replace("?ptn=", "").strip()

        # Kode resmi 4 digit di kolom ke-2
        kode_resmi = cells[1].get_text(strip=True)

        # Nama PTN di kolom ke-3
        nama_ptn = ""
        for lnk in cells[2].find_all("a", href=True):
            txt = lnk.get_text(strip=True)
            if not txt.startswith("http") and len(txt) > 3:
                nama_ptn = txt
                break
        if not nama_ptn:
            nama_ptn = cells[2].get_text(separator=" ", strip=True).split("(")[0].strip()

        if kode_ptn and kode_ptn.lstrip("-").isdigit() and nama_ptn:
            ptn_list.append({
                "kode_ptn":   kode_ptn,
                "kode_resmi": kode_resmi,
                "nama_ptn":   nama_ptn,
                "kategori":   nama_kat,
            })

    seen   = set()
    unique = []
    for p in ptn_list:
        if p["kode_ptn"] not in seen:
            seen.add(p["kode_ptn"])
            unique.append(p)

    print("    Ditemukan:", len(unique), "PTN")
    for p in unique[:3]:
        print("     ptn=" + p["kode_ptn"], "|", p["kode_resmi"], "|", p["nama_ptn"])
    if len(unique) > 3:
        print("     ... dan", len(unique)-3, "lainnya")

    return unique


# ─────────────────────────────────────────────
# TAHAP 2: Buka ptn_sn.php?ptn=111 -> ambil tabel DAFTAR PRODI
# Struktur tabel: NO | KODE | NAMA | JENJANG | DAYA TAMPUNG 2026 | PEMINAT 2025 | JENIS PORTOFOLIO
# ─────────────────────────────────────────────

def scrape_prodi(kode_ptn, kode_resmi, nama_ptn, kategori, idx, total):
    print("["+str(idx)+"/"+str(total)+"]", nama_ptn, end=" ... ", flush=True)

    soup = fetch({"ptn": kode_ptn})
    if not soup:
        print("GAGAL")
        return []

    # Cari tabel yang punya header DAYA TAMPUNG / PEMINAT
    prodi_table = None
    for table in soup.find_all("table"):
        ths = " ".join([th.get_text(strip=True).upper() for th in table.find_all("th")])
        if "TAMPUNG" in ths and "PEMINAT" in ths:
            prodi_table = table
            break

    if not prodi_table:
        print("tabel prodi tidak ditemukan")
        return []

    # Map kolom berdasarkan header
    # NO | KODE | NAMA | JENJANG | DAYA TAMPUNG 2026 | PEMINAT 2025 | JENIS PORTOFOLIO
    headers_raw = []
    thead = prodi_table.find("thead")
    if thead:
        headers_raw = [th.get_text(strip=True).upper() for th in thead.find_all(["th","td"])]
    if not headers_raw:
        first_row = prodi_table.find("tr")
        if first_row:
            headers_raw = [td.get_text(strip=True).upper() for td in first_row.find_all(["th","td"])]

    col_map = {}
    for i, h in enumerate(headers_raw):
        if h in ("NO", "NO."):
            col_map[i] = "no"
        elif h == "KODE":
            col_map[i] = "kode_prodi"
        elif h in ("NAMA", "NAMA PRODI", "PROGRAM STUDI"):
            col_map[i] = "nama_prodi"
        elif h == "JENJANG":
            col_map[i] = "jenjang"
        elif "TAMPUNG" in h and "2026" in h:
            col_map[i] = "daya_tampung_2026"
        elif "TAMPUNG" in h and "2025" in h:
            col_map[i] = "daya_tampung_2025"
        elif "TAMPUNG" in h:
            col_map[i] = "daya_tampung_2026"
        elif "PEMINAT" in h and "2025" in h:
            col_map[i] = "peminat_2025"
        elif "PEMINAT" in h and "2024" in h:
            col_map[i] = "peminat_2024"
        elif "PEMINAT" in h:
            col_map[i] = "peminat_2025"
        elif "PORTO" in h:
            col_map[i] = "portofolio"
        else:
            col_map[i] = "kolom_" + str(i)

    # Fallback posisi default jika header kosong
    if not any(v == "daya_tampung_2026" for v in col_map.values()):
        col_map = {
            0: "no",
            1: "kode_prodi",
            2: "nama_prodi",
            3: "jenjang",
            4: "daya_tampung_2026",
            5: "peminat_2025",
            6: "portofolio",
        }

    # Ambil baris data
    tbody = prodi_table.find("tbody")
    rows  = tbody.find_all("tr") if tbody else prodi_table.find_all("tr")[1:]

    results = []
    for row in rows:
        cells = [td.get_text(strip=True) for td in row.find_all(["td","th"])]
        if not cells or all(c == "" for c in cells):
            continue
        # Skip baris header
        if cells[0].upper() in ("NO", "NO."):
            continue

        row_dict = {
            "nama_ptn":   nama_ptn,
            "kode_ptn":   kode_ptn,
            "kode_resmi": kode_resmi,
            "kategori":   kategori,
        }
        for i, val in enumerate(cells):
            col = col_map.get(i, "kolom_"+str(i))
            row_dict[col] = val

        row_dict["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append(row_dict)

    print(len(results), "prodi")
    return results


# ─────────────────────────────────────────────
# CLEAN
# ─────────────────────────────────────────────

def clean_dataframe(df):
    if df.empty:
        return df

    df = df.drop_duplicates()

    if "nama_prodi" in df.columns:
        df["nama_prodi"] = df["nama_prodi"].str.strip().str.title()
        df = df[df["nama_prodi"].str.strip() != ""]

    if "nama_ptn" in df.columns:
        df["nama_ptn"] = df["nama_ptn"].str.strip().str.title()

    for col in ["daya_tampung_2026","daya_tampung_2025","peminat_2025","peminat_2024"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str)
                       .str.replace(".", "", regex=False)
                       .str.replace(",", "", regex=False)
                       .str.strip(),
                errors="coerce"
            )

    if "jenjang" in df.columns:
        df["jenjang"] = df["jenjang"].str.strip().str.title()

    if "daya_tampung_2026" in df.columns and "peminat_2025" in df.columns:
        mask = (
            df["peminat_2025"].notna() &
            (df["peminat_2025"] > 0) &
            df["daya_tampung_2026"].notna()
        )
        df["rasio_keketatan"] = None
        df.loc[mask, "rasio_keketatan"] = (
            df.loc[mask, "daya_tampung_2026"] / df.loc[mask, "peminat_2025"]
        ).round(4)

    drop_cols = [c for c in df.columns if c.startswith("kolom_") or c == "no"]
    df = df.drop(columns=drop_cols, errors="ignore")

    return df.reset_index(drop=True)


def to_mongodb_docs(df):
    docs = []
    for _, row in df.iterrows():
        doc = {"sumber": "sidata-ptn.snpmb.id"}
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                continue
            if isinstance(val, float) and val == int(val):
                doc[col] = int(val)
            else:
                doc[col] = val
        docs.append(doc)
    return docs


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("\n" + "="*55)
    print("  SCRAPER DAYA TAMPUNG FINAL")
    print("  Proyek: EduPass")
    print("  URL: ptn_sn.php?ptn=XXX")
    print("="*55)

    # TAHAP 1
    print("\n" + "="*55)
    print("  TAHAP 1 -- Ambil daftar PTN")
    print("="*55)

    all_ptn = []
    for nama_kat, param_kat in KATEGORI:
        ptn = get_ptn_list(nama_kat, param_kat)
        all_ptn.extend(ptn)
        time.sleep(random.uniform(1.0, 2.0))

    print("\n  Total PTN:", len(all_ptn))
    if not all_ptn:
        print("[BERHENTI] Tidak ada PTN.")
        return

    # TAHAP 2
    print("\n" + "="*55)
    print("  TAHAP 2 -- Scrape prodi tiap PTN")
    print("="*55 + "\n")

    all_rows = []
    berhasil = 0
    gagal    = 0

    for idx, ptn in enumerate(all_ptn, 1):
        rows = scrape_prodi(
            ptn["kode_ptn"],
            ptn["kode_resmi"],
            ptn["nama_ptn"],
            ptn["kategori"],
            idx,
            len(all_ptn)
        )
        if rows:
            all_rows.extend(rows)
            berhasil += 1
        else:
            gagal += 1

        if idx < len(all_ptn):
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    print("\n" + "="*55)
    print("  Selesai:", berhasil, "PTN OK |", gagal, "PTN gagal")
    print("="*55)

    if not all_rows:
        print("[!] Tidak ada data.")
        return

    df = pd.DataFrame(all_rows)
    df = clean_dataframe(df)

    print("\n  Total data       :", len(df), "baris")
    print("  Total PTN        :", df["nama_ptn"].nunique() if "nama_ptn" in df.columns else "-")
    print("  Total prodi unik :", df["nama_prodi"].nunique() if "nama_prodi" in df.columns else "-")
    print("  Kolom            :", list(df.columns))

    csv_path = "daya_tampung_snbp.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print("\n  CSV  tersimpan:", csv_path)

    json_path = "daya_tampung_snbp.json"
    docs = to_mongodb_docs(df)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print("  JSON tersimpan:", json_path)

    print("\n  Preview 10 data pertama:")
    print("  " + "-"*70)
    cols = [c for c in ["nama_ptn","nama_prodi","jenjang","daya_tampung_2026","peminat_2025","rasio_keketatan"]
            if c in df.columns]
    print(df[cols].head(10).to_string(index=False))

    print("\n" + "="*55)
    print("  IMPORT KE MONGODB EDUPASS")
    print("="*55)
    print("")
    print("  mongoimport --db edupass ^")
    print("              --collection daya_tampung ^")
    print("              --file daya_tampung_snbp.json ^")
    print("              --jsonArray")
    print("")


if __name__ == "__main__":
    main()
