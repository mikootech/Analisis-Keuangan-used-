# 💰 Catatan Keuangan — Panduan Setup

Aplikasi pencatatan keuangan sederhana untuk UMKM.
Dibangun dengan Python + Streamlit + Supabase.

---

## 📋 Langkah 1 — Buat Database di Supabase (GRATIS)

1. Buka **https://supabase.com** → klik **Start for Free** → daftar akun
2. Klik **New Project** → isi nama project (contoh: `keuangan-umkm`) → pilih region **Southeast Asia**
3. Setelah project siap, klik menu **SQL Editor** di sidebar kiri
4. Copy-paste isi file `supabase_schema.sql` ke editor → klik **Run**
5. Tabel `transaksi` akan otomatis terbuat ✅

**Catat dua informasi ini** (Settings → API):
- **Project URL** → contoh: `https://abcdefgh.supabase.co`
- **anon public key** → string panjang dimulai `eyJhbGc...`

---

## 🚀 Langkah 2 — Deploy Aplikasi (GRATIS via Streamlit Cloud)

> **Catatan:** Streamlit tidak bisa di-hosting di Vercel (Vercel untuk Next.js/website statis).
> Gunakan **Streamlit Community Cloud** — sama-sama gratis, bahkan lebih mudah!

### A. Upload ke GitHub

1. Buat akun di **https://github.com** (gratis)
2. Buat repository baru → nama: `catatan-keuangan`
3. Upload semua file ini (kecuali `secrets.toml`) ke repository

**File yang perlu di-upload:**
```
app.py
requirements.txt
.streamlit/config.toml
supabase_schema.sql
```

### B. Deploy di Streamlit Cloud

1. Buka **https://streamlit.io/cloud** → Login dengan akun GitHub
2. Klik **New app** → pilih repository `catatan-keuangan`
3. Main file path: `app.py` → klik **Deploy**
4. Setelah deploy, klik **⚙️ Settings → Secrets**
5. Masukkan konfigurasi berikut (ganti dengan data Supabase Anda):

```toml
SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIs..."
```

6. Klik **Save** → aplikasi akan restart otomatis ✅

Aplikasi Anda akan dapat diakses di URL:
`https://[nama-app]-[username].streamlit.app`

---

## 💻 Langkah 3 — Jalankan di Komputer Sendiri (Opsional)

Jika ingin mencoba di laptop/komputer sebelum deploy:

```bash
# 1. Install Python 3.10+ (https://python.org)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Buat file secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml → isi SUPABASE_URL dan SUPABASE_KEY

# 4. Jalankan aplikasi
streamlit run app.py
```

Buka browser → **http://localhost:8501**

---

## 📱 Cara Pakai di HP

1. Buka URL aplikasi di browser HP (Chrome/Safari)
2. Tap ikon **...** atau **Share** → **Tambahkan ke Layar Utama**
3. Aplikasi akan muncul seperti app biasa di HP Anda ✅

---

## 🛠 Struktur File

```
catatan-keuangan/
├── app.py                          ← Aplikasi utama
├── requirements.txt                ← Daftar library Python
├── supabase_schema.sql             ← Script buat database
├── .streamlit/
│   ├── config.toml                 ← Pengaturan tampilan
│   └── secrets.toml.example        ← Contoh konfigurasi
└── README.md                       ← Panduan ini
```

---

## ❓ Pertanyaan Umum

**Q: Data saya aman?**
A: Data tersimpan di server Supabase yang aman. Hanya Anda yang bisa mengaksesnya.

**Q: Apakah berbayar?**
A: Tidak! Supabase gratis untuk data kecil (<500MB). Streamlit Cloud juga gratis.

**Q: Bisa pakai HP dan laptop sekaligus?**
A: Bisa! Data otomatis tersinkron karena tersimpan di cloud.

**Q: Bagaimana jika lupa keterangan?**
A: Kolom keterangan boleh dikosongkan — tidak wajib diisi.

---

## 📞 Butuh Bantuan?

Jika ada kendala saat setup, tanyakan ke pengembang atau cari di Google:
- "cara buat project supabase"
- "cara deploy streamlit cloud"
