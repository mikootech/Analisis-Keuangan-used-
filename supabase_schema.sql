-- ============================================================
-- SKEMA DATABASE — Catatan Keuangan UMKM (dengan Login)
-- Jalankan SQL ini di: Supabase Dashboard → SQL Editor
-- ============================================================

-- ────────────────────────────────────────────────────────────
-- 1. TABEL USERS
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.users (
    id          BIGSERIAL PRIMARY KEY,
    username    VARCHAR(50)   UNIQUE NOT NULL,
    password    TEXT          NOT NULL,          -- bcrypt hashed
    role        VARCHAR(10)   DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at  TIMESTAMPTZ   DEFAULT NOW()
);

-- Aktifkan RLS pada tabel users
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Policy: semua bisa baca/tulis (karena autentikasi di level aplikasi)
CREATE POLICY "Akses publik users"
    ON public.users
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Index untuk pencarian username
CREATE INDEX IF NOT EXISTS idx_users_username
    ON public.users (username);

-- ────────────────────────────────────────────────────────────
-- 2. TABEL TRANSAKSI (dengan user_id)
-- ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.transaksi (
    id          BIGSERIAL PRIMARY KEY,
    tanggal     DATE          NOT NULL,
    jenis       VARCHAR(20)   NOT NULL CHECK (jenis IN ('pengeluaran', 'pemasukan')),
    kategori    VARCHAR(20)   NOT NULL CHECK (kategori IN ('warung', 'pribadi')),
    keterangan  TEXT          DEFAULT '',
    jumlah      NUMERIC(15,2) NOT NULL CHECK (jumlah > 0),
    user_id     BIGINT        REFERENCES public.users(id) ON DELETE CASCADE,
    created_at  TIMESTAMPTZ   DEFAULT NOW()
);

-- Aktifkan Row Level Security (RLS)
ALTER TABLE public.transaksi ENABLE ROW LEVEL SECURITY;

-- Izinkan akses publik (autentikasi di level aplikasi Streamlit)
CREATE POLICY "Akses publik transaksi"
    ON public.transaksi
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Index agar query tanggal lebih cepat
CREATE INDEX IF NOT EXISTS idx_transaksi_tanggal
    ON public.transaksi (tanggal DESC);

-- Index untuk query per user
CREATE INDEX IF NOT EXISTS idx_transaksi_user_id
    ON public.transaksi (user_id);

-- ============================================================
-- CATATAN MIGRASI (jika tabel transaksi sudah ada):
--
-- Jalankan perintah ini satu per satu di SQL Editor:
--
-- ALTER TABLE public.transaksi
--     ADD COLUMN IF NOT EXISTS user_id BIGINT
--     REFERENCES public.users(id) ON DELETE CASCADE;
--
-- CREATE INDEX IF NOT EXISTS idx_transaksi_user_id
--     ON public.transaksi (user_id);
--
-- ============================================================
-- SEED ADMIN ACCOUNT:
--
-- Password: admin102938182930
-- Hash di-generate oleh aplikasi saat pertama kali dijalankan.
-- Atau insert manual (ganti $BCRYPT_HASH dengan hasil hash):
--
-- INSERT INTO public.users (username, password, role)
-- VALUES ('admin', '$BCRYPT_HASH', 'admin')
-- ON CONFLICT (username) DO NOTHING;
-- ============================================================
