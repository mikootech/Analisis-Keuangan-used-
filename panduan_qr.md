# 📱 Panduan Scan QR Code — Catatan Keuangan UMKM

## Apa itu QR Code untuk Web App?

QR Code adalah barcode 2D yang bisa di-scan menggunakan kamera HP. Ketika di-scan,
HP akan langsung membuka URL web aplikasi Catatan Keuangan Anda — tanpa perlu
mengetik alamat web secara manual.

---

## 🚀 Cara Generate QR Code

### Cara 1: Melalui Admin Panel (Otomatis)

1. **Login sebagai Admin** di web app
2. Buka tab **🔗 QR Code**
3. Masukkan URL deploy web app Anda (contoh: `https://nama-app.streamlit.app`)
4. Klik **Generate QR Code**
5. QR code akan muncul — bisa di-download sebagai gambar PNG

### Cara 2: Menggunakan Website Online

1. Buka [qr-code-generator.com](https://www.qr-code-generator.com/) atau [qrcode-monkey.com](https://www.qrcode-monkey.com/)
2. Pilih tipe **URL**
3. Masukkan URL deploy web app Anda
4. Klik Generate → Download

### Cara 3: Menggunakan Google Chrome

1. Buka web app Anda di Google Chrome
2. Klik ikon **Share** (⫶) di address bar
3. Pilih **Create QR Code**
4. Download gambar QR

---

## 📲 Cara Scan QR Code di HP

### Android
1. Buka **Kamera** bawaan HP
2. Arahkan kamera ke QR Code
3. Ketuk notifikasi link yang muncul
4. Web app akan terbuka di browser

> 💡 Jika kamera bawaan tidak bisa scan QR, download app **Google Lens** dari Play Store.

### iPhone (iOS)
1. Buka **Kamera** bawaan
2. Arahkan ke QR Code
3. Ketuk banner link yang muncul di atas layar
4. Safari akan membuka web app

---

## 🖨️ Tips Penggunaan QR Code

### Untuk Display di Toko/Warung
1. **Print QR code** ukuran besar (minimal 5x5 cm)
2. Tempel di lokasi strategis:
   - Di kasir
   - Di meja kerja
   - Di dinding dekat pintu masuk
3. Tambahkan teks: *"Scan untuk akses Catatan Keuangan"*

### Untuk Sharing ke Karyawan
1. Generate QR code dari admin panel
2. Kirim gambar QR via **WhatsApp** atau **Telegram**
3. Karyawan scan → langsung bisa login dengan akun masing-masing

### Bookmark di HP (PWA-like)
Setelah membuka web app via QR code:

**Android:**
1. Ketuk menu ⋮ di Chrome
2. Pilih **"Add to Home Screen"**
3. Beri nama → Ketuk **Add**
4. Icon app akan muncul di home screen

**iPhone:**
1. Ketuk ikon **Share** (⬆️) di Safari
2. Scroll ke bawah → pilih **"Add to Home Screen"**
3. Beri nama → ketuk **Add**

---

## 🔗 URL Deploy

Jika Anda deploy di **Streamlit Community Cloud**, URL-nya berbentuk:
```
https://[nama-github-user]-[nama-repo]-[nama-file]-[hash].streamlit.app
```

Jika Anda deploy di **server sendiri**, gunakan IP/domain server Anda:
```
http://[IP-server]:8501
```

---

## ❓ FAQ

**Q: Apakah QR Code-nya berubah jika saya update kode?**
A: Tidak. Selama URL deploy-nya sama, QR code tetap valid.

**Q: Bisa diakses tanpa internet?**
A: Tidak. Web app membutuhkan koneksi internet untuk mengakses database Supabase.

**Q: Aman tidak jika orang lain scan QR code saya?**
A: Aman, karena sudah ada sistem login. Orang yang scan tetap harus login untuk mengakses data.
