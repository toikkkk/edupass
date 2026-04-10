import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime

BASE_URL  = "https://haipintar.com"
INDEX_URL = "https://haipintar.com/nilai-siswa-eligible/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/",
}

DELAY_MIN = 2.0
DELAY_MAX = 4.5


def fetch_page(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "lxml")
    except requests.exceptions.HTTPError as e:
        print("    [HTTP ERROR]", e)
    except requests.exceptions.ConnectionError:
        print("    [CONNECTION ERROR] Tidak bisa terhubung:", url)
    except requests.exceptions.Timeout:
        print("    [TIMEOUT]", url)
    except Exception as e:
        print("    [ERROR]", e)
    return None


def scrape_index_page():
    print("\n" + "="*55)
    print("  TAHAP 1 -- Ambil daftar PTN")
    print("  URL:", INDEX_URL)
    print("="*55)

    soup = fetch_page(INDEX_URL)
    if soup is None:
        print("  [GAGAL] Halaman index tidak bisa diakses.")
        return []

    ptn_list = []
    all_links = soup.find_all("a", href=True)
    lihat_links = [
        a for a in all_links
        if "lihat" in a.get_text(strip=True).lower()
        or "nilai" in a.get("href", "").lower()
        or "snbp"  in a.get("href", "").lower()
    ]

    for link in lihat_links:
        href       = link["href"]
        url_detail = href if href.startswith("http") else BASE_URL + href
        parent_row = link.find_parent("tr")
        nama_ptn   = ""
        akronim    = ""

        if parent_row:
            cells = parent_row.find_all(["td", "th"])
            texts = [c.get_text(strip=True) for c in cells]
            for t in texts:
                if not t or t.isdigit():
                    continue
                if t.lower() in ("lihat nilai", "lihat", "-"):
                    continue
                if t.isupper() and 2 <= len(t) <= 20:
                    akronim = t
                elif not nama_ptn and len(t) > 3:
                    nama_ptn = t

        if not nama_ptn:
            slug     = url_detail.rstrip("/").split("/")[-1]
            nama_ptn = slug.replace("rata-rata-nilai-snbp-", "").replace("-", " ").title()

        ptn_list.append({
            "nama_ptn":   nama_ptn,
            "akronim":    akronim,
            "url_detail": url_detail,
        })

    seen   = set()
    unique = []
    for item in ptn_list:
        if item["url_detail"] not in seen:
            seen.add(item["url_detail"])
            unique.append(item)

    print("\n  Ditemukan", len(unique), "PTN")
    for i, p in enumerate(unique[:5], 1):
        print("   ", i, p["nama_ptn"], "("+p["akronim"]+")")
        print("        URL:", p["url_detail"])
    if len(unique) > 5:
        print("    ... dan", len(unique)-5, "PTN lainnya")

    return unique


def scrape_detail_page(nama_ptn, akronim, url):
    soup = fetch_page(url)
    if soup is None:
        return []

    results = []
    tables  = soup.find_all("table")

    if not tables:
        print("    [WARNING] Tidak ada tabel di halaman", nama_ptn)
        return []

    for table in tables:
        headers_raw = []
        thead = table.find("thead")
        if thead:
            headers_raw = [th.get_text(strip=True) for th in thead.find_all(["th", "td"])]
        if not headers_raw:
            first_row = table.find("tr")
            if first_row:
                headers_raw = [td.get_text(strip=True) for td in first_row.find_all(["th", "td"])]

        col_map = {}
        for i, h in enumerate(headers_raw):
            hl = h.lower()
            if any(k in hl for k in ["jurusan", "prodi", "program", "nama"]):
                col_map[i] = "nama_prodi"
            elif any(k in hl for k in ["jenjang", "level", "strata"]):
                col_map[i] = "jenjang"
            elif any(k in hl for k in ["nilai", "rata", "skor", "snbp"]):
                col_map[i] = "nilai_rata_rata"
            else:
                col_map[i] = "kolom_" + str(i)

        tbody = table.find("tbody")
        rows  = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

        for row in rows:
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if not cells or all(c == "" for c in cells):
                continue

            row_dict = {"nama_ptn": nama_ptn, "akronim": akronim}

            for i, val in enumerate(cells):
                col_name = col_map.get(i, "kolom_" + str(i))
                row_dict[col_name] = val

            raw_nilai = row_dict.get("nilai_rata_rata", "")
            if raw_nilai:
                try:
                    row_dict["nilai_rata_rata"] = float(
                        str(raw_nilai).replace(",", ".").strip()
                    )
                except ValueError:
                    for k, v in row_dict.items():
                        try:
                            fv = float(str(v).replace(",", ".").strip())
                            if 60.0 <= fv <= 100.0:
                                row_dict["nilai_rata_rata"] = fv
                                break
                        except (ValueError, TypeError):
                            continue

            row_dict["url_sumber"] = url
            row_dict["scraped_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            results.append(row_dict)

    return results


def clean_dataframe(df):
    if df.empty:
        return df
    df = df.drop_duplicates()
    if "nama_prodi" in df.columns:
        df["nama_prodi"] = df["nama_prodi"].str.strip().str.title()
        df = df[df["nama_prodi"].str.strip() != ""]
    if "nilai_rata_rata" in df.columns:
        df["nilai_rata_rata"] = pd.to_numeric(df["nilai_rata_rata"], errors="coerce")
        df = df.dropna(subset=["nilai_rata_rata"])
        df = df[(df["nilai_rata_rata"] >= 60) & (df["nilai_rata_rata"] <= 100)]
    if "jenjang" in df.columns:
        df["jenjang"] = df["jenjang"].str.upper().str.strip()
    sort_cols = [c for c in ["nama_ptn", "jenjang", "nilai_rata_rata"] if c in df.columns]
    if sort_cols:
        asc = [True] * (len(sort_cols) - 1) + [False]
        df  = df.sort_values(sort_cols, ascending=asc)
    return df.reset_index(drop=True)


def to_mongodb_docs(df):
    docs = []
    for _, row in df.iterrows():
        doc = {
            "nama_ptn":        str(row.get("nama_ptn", "")).strip(),
            "akronim":         str(row.get("akronim", "")).strip(),
            "nama_prodi":      str(row.get("nama_prodi", "")).strip(),
            "jenjang":         str(row.get("jenjang", "S1")).strip() or "S1",
            "nilai_rata_rata": float(row.get("nilai_rata_rata", 0)),
            "sumber":          "haipintar.com",
            "url_sumber":      str(row.get("url_sumber", "")),
            "scraped_at":      str(row.get("scraped_at", "")),
        }
        doc = {k: v for k, v in doc.items() if str(v) not in ("", "nan", "None")}
        docs.append(doc)
    return docs


def main():
    print("\n" + "="*55)
    print("  SCRAPER v2 -- haipintar.com Nilai Siswa Eligible")
    print("  Proyek: EduPass")
    print("="*55)

    ptn_list = scrape_index_page()
    if not ptn_list:
        print("\n[BERHENTI] Tidak ada PTN yang ditemukan.")
        return

    print("\n" + "="*55)
    print("  TAHAP 2 -- Ambil nilai tiap PTN")
    print("="*55)

    all_rows = []
    berhasil = 0
    gagal    = 0

    for idx, ptn in enumerate(ptn_list, 1):
        nama = ptn["nama_ptn"]
        akr  = ptn["akronim"]
        url  = ptn["url_detail"]

        print("\n[" + str(idx) + "/" + str(len(ptn_list)) + "]", nama, "("+akr+")")
        print("  URL:", url)

        rows = scrape_detail_page(nama, akr, url)

        if rows:
            all_rows.extend(rows)
            berhasil += 1
            print("  OK --", len(rows), "prodi ditemukan")
        else:
            gagal += 1
            print("  SKIP -- tidak ada data")

        if idx < len(ptn_list):
            delay = random.uniform(DELAY_MIN, DELAY_MAX)
            print("  Jeda", round(delay, 1), "detik...")
            time.sleep(delay)

    print("\n" + "="*55)
    print("  Selesai:", berhasil, "PTN OK |", gagal, "PTN gagal/skip")
    print("="*55)

    if not all_rows:
        print("\n[!] Tidak ada data berhasil di-scrape.")
        print("    Kemungkinan penyebab:")
        print("    1. Website memblokir -- coba ganti User-Agent")
        print("    2. Struktur HTML berubah -- cek manual di browser")
        print("    3. Koneksi internet bermasalah")
        return

    df = pd.DataFrame(all_rows)
    df = clean_dataframe(df)

    print("\n  Total data   :", len(df), "baris")
    print("  Total PTN    :", df["nama_ptn"].nunique() if "nama_ptn" in df.columns else "-")
    print("  Total prodi  :", df["nama_prodi"].nunique() if "nama_prodi" in df.columns else "-")

    csv_path = "nilai_eligible_snbp.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print("\n  CSV  tersimpan :", csv_path)

    json_path = "nilai_eligible_snbp.json"
    docs = to_mongodb_docs(df)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print("  JSON tersimpan :", json_path)

    print("\n  Preview 10 data pertama:")
    print("  " + "-"*60)
    cols = [c for c in ["nama_ptn", "akronim", "nama_prodi", "jenjang", "nilai_rata_rata"]
            if c in df.columns]
    print(df[cols].head(10).to_string(index=False))


if __name__ == "__main__":
    main()