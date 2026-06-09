import streamlit as st
import os
import re
from supabase import create_client
import pandas as pd
import uuid
from datetime import date, datetime, timedelta
import io
import html as html_lib
import bcrypt
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN  (harus paling pertama)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Catatan Keuangan",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────────────────────
# CSS  — desain minimalis, ramah HP + halaman login premium
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Font ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Layout utama ── */
.main .block-container {
    padding: 1rem 1rem 4rem 1rem !important;
    max-width: 480px !important;
}

/* ── Sembunyikan elemen bawaan Streamlit ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Header aplikasi ── */
.app-header {
    text-align: center;
    padding: 12px 0 18px 0;
}
.app-title {
    font-size: 22px;
    font-weight: 800;
    color: #1a1a2e;
    margin: 0;
    letter-spacing: -0.3px;
}
.app-sub {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 3px;
    letter-spacing: 0.1px;
}

/* ── Tab bar ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 3px;
    background: #f3f4f6;
    border-radius: 12px;
    padding: 3px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    font-size: 12.5px;
    font-weight: 600;
    padding: 7px 10px;
    color: #9ca3af;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: #1a1a2e !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1) !important;
}

/* ── Kartu metrik (2 kotak header) ── */
.cards-row {
    display: flex;
    gap: 10px;
    margin: 10px 0 10px 0;
}
.card-expense {
    flex: 1;
    background: #fff7f7;
    border: 1.5px solid #fde8e8;
    border-radius: 14px;
    padding: 13px 12px;
}
.card-income {
    flex: 1;
    background: #f6fef7;
    border: 1.5px solid #d6f5da;
    border-radius: 14px;
    padding: 13px 12px;
}
.card-label {
    font-size: 10.5px;
    font-weight: 700;
    color: #b0b7c3;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
}
.card-val-expense {
    font-size: 18px;
    font-weight: 800;
    color: #d96060;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.card-val-income {
    font-size: 18px;
    font-weight: 800;
    color: #4caf50;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.card-note {
    font-size: 10px;
    color: #d1d5db;
    margin-top: 3px;
}

/* ── Chip saldo ── */
.balance-chip {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 9px 14px;
    text-align: center;
    margin-bottom: 14px;
    font-size: 12.5px;
    color: #9ca3af;
}
.balance-chip strong {
    font-size: 15px;
    font-weight: 700;
    margin-left: 5px;
}

/* ── Judul seksi ── */
.section-title {
    font-size: 13px;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 14px 0 8px 0;
}
.form-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 14px;
}

/* ── Item transaksi ── */
.trx-expense {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(217, 96, 96, 0.055);
    border-left: 3px solid #d96060;
    border-radius: 0 10px 10px 0;
    padding: 9px 11px;
    margin: 4px 0;
}
.trx-income {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(76, 175, 80, 0.055);
    border-left: 3px solid #4caf50;
    border-radius: 0 10px 10px 0;
    padding: 9px 11px;
    margin: 4px 0;
}
.trx-desc {
    font-size: 13.5px;
    font-weight: 600;
    color: #1a1a2e;
    max-width: 175px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.trx-meta {
    display: flex;
    gap: 5px;
    align-items: center;
    margin-top: 2px;
}
.trx-date {
    font-size: 10.5px;
    color: #c4c9d4;
}
.trx-badge {
    font-size: 9.5px;
    background: #f3f4f6;
    color: #9ca3af;
    border-radius: 4px;
    padding: 1px 5px;
    font-weight: 600;
}
.trx-amt-expense {
    font-size: 13.5px;
    font-weight: 700;
    color: #d96060;
    white-space: nowrap;
    letter-spacing: -0.3px;
}
.trx-amt-income {
    font-size: 13.5px;
    font-weight: 700;
    color: #4caf50;
    white-space: nowrap;
    letter-spacing: -0.3px;
}

/* ── Banner sukses ── */
.success-banner {
    background: #f0fff4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 11px 14px;
    text-align: center;
    color: #166534;
    font-weight: 600;
    font-size: 13.5px;
    margin-bottom: 14px;
}

/* ── State kosong ── */
.empty-state {
    text-align: center;
    padding: 28px 16px;
    color: #c4c9d4;
    font-size: 13px;
    line-height: 1.6;
}

/* ── Judul laporan ── */
.report-title-box {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 11px 14px;
    margin: 10px 0 12px 0;
}
.report-title-main {
    font-size: 12.5px;
    font-weight: 700;
    color: #374151;
    letter-spacing: 0.1px;
}
.report-title-range {
    font-size: 12px;
    color: #9ca3af;
    margin-top: 2px;
}

/* ── Tombol ── */
.stButton > button {
    border-radius: 11px !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 10px 0 !important;
    font-size: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.1px;
    transition: all 0.15s ease !important;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #f0f0f2;
    margin: 14px 0;
}

/* ── Input fields ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 9px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ══════════════════════════════════════════════════════════════
   HALAMAN LOGIN — DESAIN PREMIUM
   ══════════════════════════════════════════════════════════════ */

.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 0 8px;
}

.login-hero {
    text-align: center;
    padding: 30px 0 24px 0;
}

.login-icon {
    font-size: 48px;
    margin-bottom: 10px;
    display: block;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

.login-hero-title {
    font-size: 24px;
    font-weight: 800;
    color: #1a1a2e;
    margin: 0;
    letter-spacing: -0.5px;
}

.login-hero-sub {
    font-size: 13px;
    color: #9ca3af;
    margin-top: 6px;
    line-height: 1.4;
}

.login-card {
    background: #ffffff;
    border: 1.5px solid #e5e7eb;
    border-radius: 18px;
    padding: 24px 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.04);
}

.login-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 4px;
}

.login-card-sub {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 16px;
}

.login-footer {
    text-align: center;
    padding: 16px 0;
    font-size: 11.5px;
    color: #d1d5db;
}

/* ── Admin panel ── */
.admin-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #2d2b55 100%);
    border-radius: 16px;
    padding: 20px 18px;
    margin-bottom: 16px;
    color: white;
}

.admin-header-title {
    font-size: 18px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.3px;
}

.admin-header-sub {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    margin-top: 3px;
}

.user-card {
    background: #ffffff;
    border: 1.5px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px 14px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.15s ease;
}

.user-card:hover {
    border-color: #c7d2fe;
    box-shadow: 0 2px 12px rgba(99,102,241,0.08);
}

.user-name {
    font-size: 14px;
    font-weight: 700;
    color: #1a1a2e;
}

.user-role {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 6px;
}

.role-admin {
    background: #fef3c7;
    color: #d97706;
}

.role-user {
    background: #e0e7ff;
    color: #4f46e5;
}

.user-date {
    font-size: 10.5px;
    color: #c4c9d4;
    margin-top: 2px;
}

/* ── Stat cards admin ── */
.stat-row {
    display: flex;
    gap: 8px;
    margin: 12px 0;
}
.stat-card {
    flex: 1;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 12px 10px;
    text-align: center;
}
.stat-num {
    font-size: 22px;
    font-weight: 800;
    color: #1a1a2e;
}
.stat-label {
    font-size: 10px;
    font-weight: 600;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-top: 2px;
}

/* ── User info sidebar ── */
.sidebar-user {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
    text-align: center;
}
.sidebar-avatar {
    width: 48px;
    height: 48px;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 8px auto;
    font-size: 20px;
    color: white;
    font-weight: 700;
}
.sidebar-name {
    font-size: 14px;
    font-weight: 700;
    color: #1a1a2e;
}
.sidebar-role-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 6px;
    margin-top: 4px;
}

/* ── Logout button di header ── */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.header-bar .app-header {
    padding: 12px 0 8px 0;
    text-align: left;
    flex: 1;
}
.logout-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f9fafb;
    border: 1.5px solid #e5e7eb;
    border-radius: 10px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
    color: #9ca3af;
    cursor: pointer;
    transition: all 0.15s ease;
    text-decoration: none;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.logout-btn:hover {
    background: #fff5f5;
    border-color: #fecaca;
    color: #d96060;
}

/* ── Error/warning banner ── */
.error-banner {
    background: #fff5f5;
    border: 1px solid #fecaca;
    border-radius: 10px;
    padding: 11px 14px;
    text-align: center;
    color: #991b1b;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 14px;
}

.warning-banner {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 11px 14px;
    text-align: center;
    color: #92400e;
    font-weight: 600;
    font-size: 13px;
    margin-bottom: 14px;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# KONEKSI SUPABASE
# ─────────────────────────────────────────────────────────────────────────────
def _clean_supabase_url(url: str) -> str:
    """Bersihkan URL Supabase — hapus /rest/v1/ jika ada di akhir."""
    url = url.strip().rstrip("/")
    # Hapus /rest/v1 di akhir URL jika ada (penyebab double-path error)
    url = re.sub(r'/rest/v1/?$', '', url)
    return url

@st.cache_resource
def get_supabase():
    # Coba dari st.secrets dulu, fallback ke os.environ
    try:
        url = st.secrets["SUPABASE_URL"]
    except (KeyError, FileNotFoundError):
        url = os.environ.get("SUPABASE_URL", "")
    try:
        key = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError):
        key = os.environ.get("SUPABASE_KEY", "")

    if not url or not key:
        raise ValueError("SUPABASE_URL dan SUPABASE_KEY harus diisi di secrets.toml atau environment variables!")

    url = _clean_supabase_url(url)
    return create_client(url, key)

try:
    sb = get_supabase()
except Exception as e:
    st.error(f"⚠️ Gagal terhubung ke database: {e}")
    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# AUTH FUNCTIONS — HASH, VERIFY, REGISTER, LOGIN
# ─────────────────────────────────────────────────────────────────────────────

# Admin credentials — bisa di-override via secrets
def _get_admin_username():
    try:
        return st.secrets.get("ADMIN_USERNAME", "admin")
    except (KeyError, FileNotFoundError):
        return os.environ.get("ADMIN_USERNAME", "admin")

def _get_admin_password():
    try:
        return st.secrets.get("ADMIN_PASSWORD", "admin102938182930")
    except (KeyError, FileNotFoundError):
        return os.environ.get("ADMIN_PASSWORD", "admin102938182930")

ADMIN_DEFAULT_USERNAME = _get_admin_username()
ADMIN_DEFAULT_PASSWORD = _get_admin_password()

def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """Verifikasi password terhadap hash bcrypt."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def ensure_admin_exists():
    """Pastikan akun admin default ada di database. Reset password jika corrupt."""
    try:
        r = sb.table("users").select("id,password").eq("username", ADMIN_DEFAULT_USERNAME).execute()
        if not r.data:
            # Admin belum ada → buat baru
            hashed = hash_password(ADMIN_DEFAULT_PASSWORD)
            sb.table("users").insert({
                "username": ADMIN_DEFAULT_USERNAME,
                "password": hashed,
                "role": "admin",
            }).execute()
        else:
            # Admin sudah ada → cek apakah password hash masih valid
            admin_row = r.data[0]
            if not verify_password(ADMIN_DEFAULT_PASSWORD, admin_row["password"]):
                # Password hash corrupt atau tidak cocok → reset
                new_hash = hash_password(ADMIN_DEFAULT_PASSWORD)
                sb.table("users").update({
                    "password": new_hash
                }).eq("id", admin_row["id"]).execute()
    except Exception as e:
        st.warning(f"⚠️ Gagal menyiapkan akun admin: {e}")

def register_user(username: str, password: str) -> tuple[bool, str]:
    """Daftarkan user baru. Return (success, message)."""
    username = username.strip().lower()
    if len(username) < 3:
        return False, "Username minimal 3 karakter!"
    if len(password) < 6:
        return False, "Password minimal 6 karakter!"
    if username == "admin":
        return False, "Username 'admin' sudah digunakan!"
    try:
        existing = sb.table("users").select("id").eq("username", username).execute()
        if existing.data:
            return False, f"Username '{username}' sudah terdaftar!"
        hashed = hash_password(password)
        sb.table("users").insert({
            "username": username,
            "password": hashed,
            "role": "user",
        }).execute()
        return True, "Akun berhasil dibuat! Silakan login."
    except Exception as e:
        return False, f"Gagal mendaftar: {e}"

def login_user(username: str, password: str) -> tuple[bool, dict | str]:
    """Login user. Return (success, user_dict | error_message)."""
    username = username.strip().lower()
    if not username or not password:
        return False, "Username dan password wajib diisi!"
    try:
        r = sb.table("users").select("*").eq("username", username).execute()
        if not r.data:
            return False, "Username tidak ditemukan!"
        user = r.data[0]
        if not verify_password(password, user["password"]):
            return False, "Password salah!"
        return True, user
    except Exception as e:
        return False, f"Gagal login: {e}"

def get_all_users() -> list:
    """Ambil semua user dari database."""
    try:
        r = sb.table("users").select("*").order("created_at", desc=False).execute()
        return r.data or []
    except Exception:
        return []

def delete_user_db(user_id: int) -> bool:
    """Hapus user dari database (beserta transaksinya via CASCADE)."""
    try:
        sb.table("users").delete().eq("id", user_id).execute()
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
# HELPER — FORMAT & TANGGAL
# ─────────────────────────────────────────────────────────────────────────────
BULAN_ID = {
    1:"Januari", 2:"Februari", 3:"Maret",    4:"April",
    5:"Mei",     6:"Juni",     7:"Juli",      8:"Agustus",
    9:"September",10:"Oktober",11:"November",12:"Desember",
}

def fmt_rp(n: float) -> str:
    """Format singkat: Rp 1,5jt / Rp 250.000"""
    n = float(n)
    if n >= 1_000_000_000:
        v = n / 1_000_000_000
        return f"Rp {int(v)}M" if v == int(v) else f"Rp {v:.1f}M".replace(".", ",")
    if n >= 1_000_000:
        v = n / 1_000_000
        return f"Rp {int(v)}jt" if v == int(v) else f"Rp {v:.1f}jt".replace(".", ",")
    return f"Rp {int(n):,}".replace(",", ".")

def fmt_rp_full(n: float) -> str:
    """Format penuh: Rp 1.500.000"""
    return f"Rp {int(n):,}".replace(",", ".")

def fmt_date_id(d) -> str:
    """Format tanggal Indonesia: 01 Januari 2025"""
    return f"{d.day:02d} {BULAN_ID[d.month]} {d.year}"


# ─────────────────────────────────────────────────────────────────────────────
# FUNGSI DATABASE — TRANSAKSI (multi-user)
# ─────────────────────────────────────────────────────────────────────────────
def load_trx(user_id: int = None, start: date = None, end: date = None) -> pd.DataFrame:
    """Ambil transaksi dari Supabase, filter by user_id jika diberikan."""
    try:
        q = (sb.table("transaksi")
               .select("*")
               .order("tanggal", desc=True)
               .order("created_at", desc=True))
        if user_id is not None:
            q = q.eq("user_id", user_id)
        if start:
            q = q.gte("tanggal", str(start))
        if end:
            q = q.lte("tanggal", str(end))
        r = q.execute()
        if not r.data:
            return pd.DataFrame()
        df = pd.DataFrame(r.data)
        df["tanggal"] = pd.to_datetime(df["tanggal"])
        df["jumlah"]  = pd.to_numeric(df["jumlah"])
        return df
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

def save_trx(tanggal, jenis, kategori, keterangan, jumlah, user_id: int) -> bool:
    """Simpan transaksi ke Supabase dengan user_id."""
    try:
        sb.table("transaksi").insert({
            "tanggal":    str(tanggal),
            "jenis":      jenis,
            "kategori":   kategori,
            "keterangan": keterangan.strip() if keterangan else "",
            "jumlah":     float(jumlah),
            "user_id":    user_id,
        }).execute()
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan: {e}")
        return False

def delete_trx(trx_id: int) -> bool:
    """Hapus satu transaksi berdasarkan ID."""
    try:
        sb.table("transaksi").delete().eq("id", trx_id).execute()
        return True
    except Exception as e:
        st.error(f"Gagal menghapus: {e}")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# RENDER ITEM TRANSAKSI
# ─────────────────────────────────────────────────────────────────────────────
def render_trx(row) -> str:
    tgl   = row["tanggal"].strftime("%d/%m/%Y")
    ket   = html_lib.escape(str(row.get("keterangan") or "Tanpa keterangan"))
    kat   = row["kategori"].title()
    jml   = fmt_rp(row["jumlah"])
    cls   = "expense" if row["jenis"] == "pengeluaran" else "income"
    sign  = "−" if row["jenis"] == "pengeluaran" else "+"
    return f"""
    <div class="trx-{cls}">
        <div>
            <div class="trx-desc">{ket}</div>
            <div class="trx-meta">
                <span class="trx-date">{tgl}</span>
                <span class="trx-badge">{kat}</span>
            </div>
        </div>
        <div class="trx-amt-{cls}">{sign}{jml}</div>
    </div>"""


# ─────────────────────────────────────────────────────────────────────────────
# GENERATE PDF
# ─────────────────────────────────────────────────────────────────────────────
def build_pdf(df: pd.DataFrame, start: date, end: date) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        rightMargin=1.8*cm, leftMargin=1.8*cm,
        topMargin=2.2*cm,   bottomMargin=2*cm,
    )
    styles = getSampleStyleSheet()
    elems  = []

    # ── Style definisi ──
    s_title = ParagraphStyle("T", parent=styles["Normal"],
        fontSize=13, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceAfter=3)
    s_sub = ParagraphStyle("S", parent=styles["Normal"],
        fontSize=9.5, alignment=TA_CENTER,
        textColor=colors.HexColor("#888888"), spaceAfter=4)
    s_date = ParagraphStyle("D", parent=styles["Normal"],
        fontSize=11, fontName="Helvetica-Bold",
        alignment=TA_CENTER, textColor=colors.HexColor("#444444"), spaceAfter=14)
    s_sec = ParagraphStyle("SEC", parent=styles["Normal"],
        fontSize=10.5, fontName="Helvetica-Bold",
        textColor=colors.HexColor("#222222"), spaceBefore=14, spaceAfter=5)
    s_foot = ParagraphStyle("FT", parent=styles["Normal"],
        fontSize=7.5, textColor=colors.HexColor("#bbbbbb"),
        alignment=TA_CENTER, spaceBefore=8)

    # ── Header ──
    elems.append(Paragraph("DATA BERDASARKAN RENTANG TANGGAL", s_title))
    elems.append(Paragraph("Laporan Keuangan UMKM", s_sub))
    elems.append(Paragraph(f"{fmt_date_id(start)}  —  {fmt_date_id(end)}", s_date))
    elems.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#eeeeee")))

    # ── Ringkasan ──
    tot_i  = df[df["jenis"]=="pemasukan"]["jumlah"].sum()  if not df.empty else 0
    tot_e  = df[df["jenis"]=="pengeluaran"]["jumlah"].sum() if not df.empty else 0
    saldo  = tot_i - tot_e
    s_clr  = colors.HexColor("#1e8449") if saldo >= 0 else colors.HexColor("#c0392b")

    elems.append(Paragraph("Ringkasan", s_sec))
    sum_data = [
        ["Keterangan", "Jumlah"],
        ["Total Pemasukan",  fmt_rp_full(tot_i)],
        ["Total Pengeluaran", fmt_rp_full(tot_e)],
        ["Saldo Bersih",     fmt_rp_full(saldo)],
    ]
    sum_tbl = Table(sum_data, colWidths=[9.5*cm, 6.5*cm])
    sum_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR",   (0,0),(-1,0), colors.white),
        ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 9.5),
        ("PADDING",     (0,0),(-1,-1), 7),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#f9fafb")]),
        ("GRID",        (0,0),(-1,-1), 0.4, colors.HexColor("#e0e0e0")),
        ("FONTNAME",    (0,3),(-1,3), "Helvetica-Bold"),
        ("TEXTCOLOR",   (1,3),(1,3),  s_clr),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
    ]))
    elems.append(sum_tbl)
    elems.append(Spacer(1, 8))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#eeeeee")))

    # ── Daftar transaksi ──
    n = len(df) if not df.empty else 0
    elems.append(Paragraph(f"Daftar Transaksi  ({n} data)", s_sec))

    if df.empty:
        elems.append(Paragraph("Tidak ada transaksi untuk rentang tanggal ini.", styles["Normal"]))
    else:
        hdr = [["No", "Tanggal", "Jenis", "Kategori", "Keterangan", "Jumlah"]]
        rows = []
        for i, (_, r) in enumerate(df.iterrows(), 1):
            rows.append([
                str(i),
                r["tanggal"].strftime("%d/%m/%Y"),
                "Pemasukan"  if r["jenis"]=="pemasukan" else "Pengeluaran",
                r["kategori"].title(),
                str(r.get("keterangan") or "")[:38],
                fmt_rp_full(r["jumlah"]),
            ])

        trx_tbl = Table(
            hdr + rows,
            colWidths=[0.7*cm, 2.2*cm, 2.5*cm, 2.1*cm, 6.0*cm, 2.7*cm],
            repeatRows=1,
        )
        cmds = [
            ("BACKGROUND",  (0,0),(-1,0), colors.HexColor("#1a1a2e")),
            ("TEXTCOLOR",   (0,0),(-1,0), colors.white),
            ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0),(-1,-1), 8),
            ("PADDING",     (0,0),(-1,-1), 5),
            ("GRID",        (0,0),(-1,-1), 0.3, colors.HexColor("#e5e7eb")),
            ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
            ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ]
        for i, r in enumerate(df.itertuples(), 1):
            if r.jenis == "pengeluaran":
                cmds += [
                    ("BACKGROUND", (0,i),(-1,i), colors.HexColor("#fff5f5")),
                    ("TEXTCOLOR",  (5,i),(5,i),  colors.HexColor("#c0392b")),
                ]
            else:
                cmds += [
                    ("BACKGROUND", (0,i),(-1,i), colors.HexColor("#f4fff5")),
                    ("TEXTCOLOR",  (5,i),(5,i),  colors.HexColor("#1e8449")),
                ]
        trx_tbl.setStyle(TableStyle(cmds))
        elems.append(trx_tbl)

    # ── Footer ──
    elems.append(Spacer(1, 16))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#eeeeee")))
    elems.append(Paragraph(
        f"Digenerate oleh Catatan Keuangan  •  {fmt_date_id(date.today())}",
        s_foot,
    ))

    doc.build(elems)
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────────────────────────────────────
# QR CODE GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def generate_qr_code(url: str) -> bytes:
    """Generate QR code sebagai PNG bytes dari URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a1a2e", back_color="white").convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


# ─────────────────────────────────────────────────────────────────────────────
# INIT — Pastikan admin ada
# ─────────────────────────────────────────────────────────────────────────────
ensure_admin_exists()


# ─────────────────────────────────────────────────────────────────────────────
# SESSION PERSISTENCE — Cache jangka pendek agar refresh tidak perlu login lagi
# ─────────────────────────────────────────────────────────────────────────────
SESSION_DURATION_MINUTES = 60  # Sesi berlaku 60 menit

@st.cache_resource
def _get_session_store():
    """Server-side session store (bertahan selama app berjalan)."""
    return {}

def create_session(user_data: dict) -> str:
    """Buat sesi baru, return token."""
    store = _get_session_store()
    # Bersihkan sesi kadaluwarsa
    expired = [k for k, v in store.items() if datetime.now() > v["expires"]]
    for k in expired:
        del store[k]
    # Buat token baru
    token = str(uuid.uuid4())
    store[token] = {
        "user": user_data,
        "expires": datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES),
    }
    return token

def get_session(token: str):
    """Ambil user dari session token. Return None jika expired/invalid."""
    store = _get_session_store()
    if token not in store:
        return None
    session = store[token]
    if datetime.now() > session["expires"]:
        del store[token]
        return None
    # Perpanjang sesi setiap kali diakses
    session["expires"] = datetime.now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    return session["user"]

def destroy_session(token: str):
    """Hapus sesi."""
    store = _get_session_store()
    store.pop(token, None)

def do_logout():
    """Logout user: hapus session, query_params, session_state."""
    token = st.query_params.get("session")
    if token:
        destroy_session(token)
    st.query_params.clear()
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    for key in list(st.session_state.keys()):
        if key not in ["logged_in", "user", "auth_page"]:
            del st.session_state[key]
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE DEFAULTS + RESTORE SESSION
# ─────────────────────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "login"

# Coba restore session dari query_params (saat tab di-refresh)
if not st.session_state["logged_in"]:
    _token = st.query_params.get("session")
    if _token:
        _restored_user = get_session(_token)
        if _restored_user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = _restored_user
        else:
            # Token expired/invalid — bersihkan
            st.query_params.clear()


# ═════════════════════════════════════════════════════════════════════════════
#  HALAMAN LOGIN / REGISTER
# ═════════════════════════════════════════════════════════════════════════════
def show_login_page():
    """Tampilkan halaman login."""
    st.markdown("""
    <div class="login-container">
        <div class="login-hero">
            <span class="login-icon">💰</span>
            <div class="login-hero-title">Catatan Keuangan</div>
            <div class="login-hero-sub">Kelola pemasukan & pengeluaran<br>usaha Anda dengan mudah</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tab Login / Daftar ──
    auth_tab1, auth_tab2 = st.tabs(["🔑 Login", "📝 Daftar Akun"])

    with auth_tab1:
        st.markdown('<div class="login-card-title">Masuk ke Akun</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card-sub">Masukkan username dan password Anda</div>', unsafe_allow_html=True)

        login_user_input = st.text_input(
            "Username",
            placeholder="Masukkan username",
            key="login_username",
        )
        login_pass_input = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password",
            key="login_password",
        )

        if st.button("🔓  Masuk", type="primary", key="btn_login"):
            if not login_user_input or not login_pass_input:
                st.markdown('<div class="error-banner">⚠️ Username dan password wajib diisi!</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Memverifikasi..."):
                    ok, result = login_user(login_user_input, login_pass_input)
                if ok:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = result
                    # Simpan sesi agar refresh tidak perlu login lagi
                    token = create_session(result)
                    st.query_params["session"] = token
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-banner">❌ {result}</div>', unsafe_allow_html=True)

    with auth_tab2:
        st.markdown('<div class="login-card-title">Buat Akun Baru</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card-sub">Daftar untuk mulai mencatat keuangan</div>', unsafe_allow_html=True)

        reg_user_input = st.text_input(
            "Username",
            placeholder="Pilih username (min. 3 karakter)",
            key="reg_username",
        )
        reg_pass_input = st.text_input(
            "Password",
            type="password",
            placeholder="Buat password (min. 6 karakter)",
            key="reg_password",
        )
        reg_pass_confirm = st.text_input(
            "Konfirmasi Password",
            type="password",
            placeholder="Ulangi password",
            key="reg_password_confirm",
        )

        if st.button("📝  Daftar Sekarang", type="primary", key="btn_register"):
            if not reg_user_input or not reg_pass_input:
                st.markdown('<div class="error-banner">⚠️ Semua field wajib diisi!</div>', unsafe_allow_html=True)
            elif reg_pass_input != reg_pass_confirm:
                st.markdown('<div class="error-banner">⚠️ Password dan konfirmasi tidak cocok!</div>', unsafe_allow_html=True)
            else:
                with st.spinner("Mendaftarkan akun..."):
                    ok, msg = register_user(reg_user_input, reg_pass_input)
                if ok:
                    st.markdown(f'<div class="success-banner">✅ {msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-banner">❌ {msg}</div>', unsafe_allow_html=True)

    st.markdown('<div class="login-footer">🔒 Password dienkripsi dengan bcrypt</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — INFO USER & LOGOUT
# ═════════════════════════════════════════════════════════════════════════════
def show_sidebar():
    """Tampilkan sidebar dengan info user & tombol logout."""
    user = st.session_state["user"]
    username = user["username"]
    role = user["role"]
    initial = username[0].upper()

    role_cls = "role-admin" if role == "admin" else "role-user"
    role_label = "Admin" if role == "admin" else "User"

    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-user">
            <div class="sidebar-avatar">{initial}</div>
            <div class="sidebar-name">{username}</div>
            <span class="sidebar-role-badge {role_cls}">{role_label}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", key="btn_logout", type="secondary"):
            do_logout()


# ═════════════════════════════════════════════════════════════════════════════
#  USER DASHBOARD — CATAT KEUANGAN
# ═════════════════════════════════════════════════════════════════════════════
def show_user_dashboard():
    """Tampilkan dashboard keuangan untuk user biasa."""
    user = st.session_state["user"]
    uid = user["id"]
    username = user["username"]

    # Header dengan tombol logout
    hdr_col1, hdr_col2 = st.columns([5, 1])
    with hdr_col1:
        st.markdown(f"""
        <div class="app-header">
            <div class="app-title">💰 Catatan Keuangan</div>
            <div class="app-sub">Halo, {html_lib.escape(username)}! Catat pemasukan & pengeluaran usaha Anda</div>
        </div>
        """, unsafe_allow_html=True)
    with hdr_col2:
        if st.button("🚪", key="btn_logout_main", help="Logout"):
            do_logout()

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Catat", "📊 Analisis", "📋 Laporan"])

    # ── TAB 1: CATAT TRANSAKSI ──
    with tab1:
        if st.session_state.get("saved_ok"):
            st.markdown('<div class="success-banner">✅ Transaksi berhasil disimpan!</div>',
                        unsafe_allow_html=True)
            st.session_state["saved_ok"] = False

        st.markdown('<div class="form-title">Tambah Transaksi</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            jenis = st.selectbox(
                "Jenis",
                ["pengeluaran", "pemasukan"],
                format_func=lambda x: "💸 Pengeluaran" if x == "pengeluaran" else "💵 Pemasukan",
                key="inp_jenis",
            )
        with col_b:
            kategori = st.selectbox(
                "Kategori",
                ["warung", "pribadi"],
                format_func=lambda x: "🏪 Warung" if x == "warung" else "👤 Pribadi",
                key="inp_kategori",
            )

        tgl = st.date_input("Tanggal", value=date.today(), key="inp_tgl")

        ket = st.text_input(
            "Keterangan (opsional)",
            placeholder="Contoh: Beli bahan baku, Bayar listrik...",
            key="inp_ket",
        )

        jml = st.number_input(
            "Jumlah (Rp)",
            min_value=0,
            step=1_000,
            format="%d",
            key="inp_jml",
        )

        if jml > 0:
            st.caption(f"💡 {fmt_rp_full(jml)}")

        if st.button("💾  Simpan Transaksi", type="primary", key="btn_simpan"):
            if jml <= 0:
                st.warning("⚠️ Masukkan jumlah uang yang valid!")
            else:
                with st.spinner("Menyimpan..."):
                    ok = save_trx(tgl, jenis, kategori, ket, jml, uid)
                if ok:
                    st.session_state["saved_ok"] = True
                    st.rerun()

        # ── 7 transaksi terbaru ──
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Transaksi Terbaru</div>', unsafe_allow_html=True)

        df_recent = load_trx(
            user_id=uid,
            start=date.today() - timedelta(days=90),
            end=date.today(),
        )

        if df_recent.empty:
            st.markdown(
                '<div class="empty-state">📭 Belum ada transaksi.<br>Mulai catat di atas! 👆</div>',
                unsafe_allow_html=True,
            )
        else:
            html_block = "".join(render_trx(row) for _, row in df_recent.head(7).iterrows())
            st.markdown(html_block, unsafe_allow_html=True)

    # ── TAB 2: ANALISIS 30 HARI ──
    with tab2:
        today    = date.today()
        d_start  = today - timedelta(days=29)
        df30     = load_trx(user_id=uid, start=d_start, end=today)

        tot_e30  = df30[df30["jenis"]=="pengeluaran"]["jumlah"].sum() if not df30.empty else 0.0
        tot_i30  = df30[df30["jenis"]=="pemasukan"]["jumlah"].sum()   if not df30.empty else 0.0
        saldo30  = tot_i30 - tot_e30
        s_clr30  = "#4caf50" if saldo30 >= 0 else "#d96060"

        st.markdown(f"""
        <div class="cards-row">
            <div class="card-expense">
                <div class="card-label">💸 Pengeluaran</div>
                <div class="card-val-expense">{fmt_rp(tot_e30)}</div>
                <div class="card-note">30 hari terakhir</div>
            </div>
            <div class="card-income">
                <div class="card-label">💵 Pemasukan</div>
                <div class="card-val-income">{fmt_rp(tot_i30)}</div>
                <div class="card-note">30 hari terakhir</div>
            </div>
        </div>
        <div class="balance-chip">
            Saldo Bersih
            <strong style="color:{s_clr30}">{fmt_rp_full(saldo30)}</strong>
        </div>
        """, unsafe_allow_html=True)

        period_lbl = f"{d_start.strftime('%d/%m/%Y')} — {today.strftime('%d/%m/%Y')}"
        st.markdown(
            f'<div class="section-title">Semua Transaksi &nbsp;·&nbsp; {period_lbl}</div>',
            unsafe_allow_html=True,
        )

        if df30.empty:
            st.markdown(
                '<div class="empty-state">📭 Tidak ada transaksi dalam 30 hari terakhir.</div>',
                unsafe_allow_html=True,
            )
        else:
            html_block = "".join(render_trx(row) for _, row in df30.iterrows())
            st.markdown(html_block, unsafe_allow_html=True)

    # ── TAB 3: LAPORAN & EXPORT PDF ──
    with tab3:
        st.markdown('<div class="form-title">Filter Data</div>', unsafe_allow_html=True)

        col_s, col_e = st.columns(2)
        with col_s:
            f_start = st.date_input(
                "Dari Tanggal",
                value=date.today() - timedelta(days=30),
                key="f_start",
            )
        with col_e:
            f_end = st.date_input(
                "Sampai Tanggal",
                value=date.today(),
                key="f_end",
            )

        col_k, col_j = st.columns(2)
        with col_k:
            f_kat = st.selectbox(
                "Kategori",
                ["semua", "warung", "pribadi"],
                format_func=lambda x: {"semua":"📂 Semua","warung":"🏪 Warung","pribadi":"👤 Pribadi"}[x],
                key="f_kat",
            )
        with col_j:
            f_jen = st.selectbox(
                "Jenis",
                ["semua", "pengeluaran", "pemasukan"],
                format_func=lambda x: {"semua":"📋 Semua","pengeluaran":"💸 Pengeluaran","pemasukan":"💵 Pemasukan"}[x],
                key="f_jen",
            )

        if st.button("🔍  Tampilkan Data", key="btn_filter"):
            if f_start > f_end:
                st.error("⚠️ Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
            else:
                df_f = load_trx(user_id=uid, start=f_start, end=f_end)
                if not df_f.empty:
                    if f_kat != "semua":
                        df_f = df_f[df_f["kategori"] == f_kat]
                    if f_jen != "semua":
                        df_f = df_f[df_f["jenis"] == f_jen]
                st.session_state["df_filter"]  = df_f
                st.session_state["fs_saved"]   = f_start
                st.session_state["fe_saved"]   = f_end

        if "df_filter" in st.session_state:
            df_show  = st.session_state["df_filter"]
            sv_start = st.session_state["fs_saved"]
            sv_end   = st.session_state["fe_saved"]
            range_str = f"{sv_start.strftime('%d/%m/%Y')} — {sv_end.strftime('%d/%m/%Y')}"

            st.markdown('<hr class="divider">', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="report-title-box">
                <div class="report-title-main">📄 DATA BERDASARKAN RENTANG TANGGAL</div>
                <div class="report-title-range">{range_str}</div>
            </div>
            """, unsafe_allow_html=True)

            if df_show.empty:
                st.markdown(
                    '<div class="empty-state">📭 Tidak ada data untuk filter ini.</div>',
                    unsafe_allow_html=True,
                )
            else:
                tot_ef = df_show[df_show["jenis"]=="pengeluaran"]["jumlah"].sum()
                tot_if = df_show[df_show["jenis"]=="pemasukan"]["jumlah"].sum()
                saldo_f = tot_if - tot_ef
                sf_clr  = "#4caf50" if saldo_f >= 0 else "#d96060"

                st.markdown(f"""
                <div class="cards-row">
                    <div class="card-expense">
                        <div class="card-label">💸 Pengeluaran</div>
                        <div class="card-val-expense">{fmt_rp(tot_ef)}</div>
                    </div>
                    <div class="card-income">
                        <div class="card-label">💵 Pemasukan</div>
                        <div class="card-val-income">{fmt_rp(tot_if)}</div>
                    </div>
                </div>
                <div class="balance-chip">
                    Saldo &nbsp;<strong style="color:{sf_clr}">{fmt_rp_full(saldo_f)}</strong>
                    &nbsp;·&nbsp; {len(df_show)} transaksi
                </div>
                """, unsafe_allow_html=True)

                html_block = "".join(render_trx(row) for _, row in df_show.iterrows())
                st.markdown(html_block, unsafe_allow_html=True)

                # ── Export PDF ──
                st.markdown('<hr class="divider">', unsafe_allow_html=True)

                if st.button("📄  Export ke PDF", key="btn_pdf"):
                    with st.spinner("Membuat PDF..."):
                        pdf_bytes = build_pdf(df_show, sv_start, sv_end)
                    fname = f"laporan_{sv_start.strftime('%d%m%Y')}_{sv_end.strftime('%d%m%Y')}.pdf"
                    st.download_button(
                        label="⬇️  Download PDF Sekarang",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        key="dl_pdf",
                    )


# ═════════════════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
def show_admin_dashboard():
    """Tampilkan admin dashboard."""
    user = st.session_state["user"]

    # Header admin dengan tombol logout
    hdr_col1, hdr_col2 = st.columns([5, 1])
    with hdr_col1:
        st.markdown("""
        <div class="admin-header">
            <div class="admin-header-title">🛡️ Admin Panel</div>
            <div class="admin-header-sub">Kelola pengguna dan data transaksi</div>
        </div>
        """, unsafe_allow_html=True)
    with hdr_col2:
        if st.button("🚪", key="btn_logout_admin", help="Logout"):
            do_logout()

    # Stats
    all_users = get_all_users()
    total_users = len([u for u in all_users if u["role"] == "user"])
    total_admins = len([u for u in all_users if u["role"] == "admin"])

    # Count all transactions
    try:
        trx_count_r = sb.table("transaksi").select("id", count="exact").execute()
        total_trx = trx_count_r.count if trx_count_r.count else 0
    except Exception:
        total_trx = 0

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">{total_users}</div>
            <div class="stat-label">User</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{total_admins}</div>
            <div class="stat-label">Admin</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{total_trx}</div>
            <div class="stat-label">Transaksi</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs admin
    adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs([
        "👥 Daftar User", "📊 Data User", "➕ Tambah Data", "🔗 QR Code"
    ])

    # ── TAB 1: DAFTAR USER ──
    with adm_tab1:
        st.markdown('<div class="form-title">Daftar Pengguna</div>', unsafe_allow_html=True)

        if not all_users:
            st.markdown('<div class="empty-state">📭 Belum ada pengguna terdaftar.</div>',
                        unsafe_allow_html=True)
        else:
            for u in all_users:
                role_cls = "role-admin" if u["role"] == "admin" else "role-user"
                role_label = "Admin" if u["role"] == "admin" else "User"
                created = u.get("created_at", "")[:10] if u.get("created_at") else "-"

                st.markdown(f"""
                <div class="user-card">
                    <div>
                        <div class="user-name">👤 {html_lib.escape(u['username'])}</div>
                        <div class="user-date">Bergabung: {created}</div>
                    </div>
                    <span class="user-role {role_cls}">{role_label}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">Hapus User</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-card-sub">⚠️ Menghapus user akan menghapus semua transaksi miliknya!</div>', unsafe_allow_html=True)

            # Daftar user yang bisa dihapus (bukan admin yang sedang login)
            deletable_users = [u for u in all_users if u["id"] != user["id"]]
            if deletable_users:
                del_options = {f"{u['username']} ({u['role']})": u["id"] for u in deletable_users}
                selected_del = st.selectbox(
                    "Pilih user untuk dihapus",
                    options=list(del_options.keys()),
                    key="del_user_select",
                )
                if st.button("🗑️  Hapus User", key="btn_del_user", type="secondary"):
                    target_id = del_options[selected_del]
                    with st.spinner("Menghapus user..."):
                        ok = delete_user_db(target_id)
                    if ok:
                        st.markdown('<div class="success-banner">✅ User berhasil dihapus!</div>',
                                    unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-banner">❌ Gagal menghapus user!</div>',
                                    unsafe_allow_html=True)
            else:
                st.caption("Tidak ada user lain yang bisa dihapus.")

    # ── TAB 2: DATA USER ──
    with adm_tab2:
        st.markdown('<div class="form-title">Lihat & Hapus Data User</div>', unsafe_allow_html=True)

        user_options = {f"{u['username']} ({u['role']})": u["id"] for u in all_users}
        # Tambahkan opsi "Semua (tanpa user_id)" untuk data lama
        user_options["📦 Data Lama (tanpa user)"] = None

        selected_view = st.selectbox(
            "Pilih user",
            options=list(user_options.keys()),
            key="view_user_select",
        )
        selected_uid = user_options[selected_view]

        col_vs, col_ve = st.columns(2)
        with col_vs:
            adm_start = st.date_input(
                "Dari",
                value=date.today() - timedelta(days=90),
                key="adm_f_start",
            )
        with col_ve:
            adm_end = st.date_input(
                "Sampai",
                value=date.today(),
                key="adm_f_end",
            )

        if st.button("🔍  Lihat Data", key="btn_adm_view"):
            if selected_uid is None:
                # Ambil data tanpa user_id (data lama)
                try:
                    q = (sb.table("transaksi")
                           .select("*")
                           .is_("user_id", "null")
                           .gte("tanggal", str(adm_start))
                           .lte("tanggal", str(adm_end))
                           .order("tanggal", desc=True))
                    r = q.execute()
                    if r.data:
                        df_adm = pd.DataFrame(r.data)
                        df_adm["tanggal"] = pd.to_datetime(df_adm["tanggal"])
                        df_adm["jumlah"] = pd.to_numeric(df_adm["jumlah"])
                    else:
                        df_adm = pd.DataFrame()
                except Exception:
                    df_adm = pd.DataFrame()
            else:
                df_adm = load_trx(user_id=selected_uid, start=adm_start, end=adm_end)
            st.session_state["adm_df"] = df_adm
            st.session_state["adm_view_user"] = selected_view

        if "adm_df" in st.session_state:
            df_adm = st.session_state["adm_df"]
            view_label = st.session_state.get("adm_view_user", "")

            st.markdown(f'<div class="section-title">Data: {html_lib.escape(view_label)}</div>',
                        unsafe_allow_html=True)

            if df_adm.empty:
                st.markdown('<div class="empty-state">📭 Tidak ada transaksi.</div>',
                            unsafe_allow_html=True)
            else:
                # Ringkasan
                tot_e_adm = df_adm[df_adm["jenis"]=="pengeluaran"]["jumlah"].sum()
                tot_i_adm = df_adm[df_adm["jenis"]=="pemasukan"]["jumlah"].sum()
                saldo_adm = tot_i_adm - tot_e_adm
                s_clr_adm = "#4caf50" if saldo_adm >= 0 else "#d96060"

                st.markdown(f"""
                <div class="cards-row">
                    <div class="card-expense">
                        <div class="card-label">💸 Pengeluaran</div>
                        <div class="card-val-expense">{fmt_rp(tot_e_adm)}</div>
                    </div>
                    <div class="card-income">
                        <div class="card-label">💵 Pemasukan</div>
                        <div class="card-val-income">{fmt_rp(tot_i_adm)}</div>
                    </div>
                </div>
                <div class="balance-chip">
                    Saldo &nbsp;<strong style="color:{s_clr_adm}">{fmt_rp_full(saldo_adm)}</strong>
                    &nbsp;·&nbsp; {len(df_adm)} transaksi
                </div>
                """, unsafe_allow_html=True)

                # Tampilkan transaksi
                html_block = "".join(render_trx(row) for _, row in df_adm.iterrows())
                st.markdown(html_block, unsafe_allow_html=True)

                # ── Hapus transaksi ──
                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div class="form-title">Hapus Transaksi</div>', unsafe_allow_html=True)

                trx_options = {}
                for _, row in df_adm.iterrows():
                    tgl_str = row["tanggal"].strftime("%d/%m/%Y")
                    ket_str = str(row.get("keterangan") or "Tanpa ket")[:30]
                    jml_str = fmt_rp(row["jumlah"])
                    jenis_icon = "💸" if row["jenis"] == "pengeluaran" else "💵"
                    label = f"{jenis_icon} {tgl_str} — {ket_str} ({jml_str})"
                    trx_options[label] = int(row["id"])

                selected_trx = st.selectbox(
                    "Pilih transaksi untuk dihapus",
                    options=list(trx_options.keys()),
                    key="del_trx_select",
                )

                if st.button("🗑️  Hapus Transaksi", key="btn_del_trx", type="secondary"):
                    trx_id = trx_options[selected_trx]
                    with st.spinner("Menghapus..."):
                        ok = delete_trx(trx_id)
                    if ok:
                        st.markdown('<div class="success-banner">✅ Transaksi berhasil dihapus!</div>',
                                    unsafe_allow_html=True)
                        # Refresh data
                        if "adm_df" in st.session_state:
                            del st.session_state["adm_df"]
                        st.rerun()
                    else:
                        st.markdown('<div class="error-banner">❌ Gagal menghapus transaksi!</div>',
                                    unsafe_allow_html=True)

    # ── TAB 3: TAMBAH DATA (admin bisa tambah transaksi untuk user mana pun) ──
    with adm_tab3:
        st.markdown('<div class="form-title">Tambah Transaksi untuk User</div>', unsafe_allow_html=True)

        # Pilih user target
        add_user_options = {f"{u['username']}": u["id"] for u in all_users}
        selected_add_user = st.selectbox(
            "Untuk user",
            options=list(add_user_options.keys()),
            key="add_trx_user",
        )
        add_uid = add_user_options[selected_add_user]

        col_aj, col_ak = st.columns(2)
        with col_aj:
            add_jenis = st.selectbox(
                "Jenis",
                ["pengeluaran", "pemasukan"],
                format_func=lambda x: "💸 Pengeluaran" if x == "pengeluaran" else "💵 Pemasukan",
                key="add_jenis",
            )
        with col_ak:
            add_kat = st.selectbox(
                "Kategori",
                ["warung", "pribadi"],
                format_func=lambda x: "🏪 Warung" if x == "warung" else "👤 Pribadi",
                key="add_kat",
            )

        add_tgl = st.date_input("Tanggal", value=date.today(), key="add_tgl")

        add_ket = st.text_input(
            "Keterangan (opsional)",
            placeholder="Contoh: Beli bahan baku...",
            key="add_ket",
        )

        add_jml = st.number_input(
            "Jumlah (Rp)",
            min_value=0,
            step=1_000,
            format="%d",
            key="add_jml",
        )

        if add_jml > 0:
            st.caption(f"💡 {fmt_rp_full(add_jml)}")

        if st.button("💾  Simpan Transaksi", type="primary", key="btn_adm_save"):
            if add_jml <= 0:
                st.warning("⚠️ Masukkan jumlah uang yang valid!")
            else:
                with st.spinner("Menyimpan..."):
                    ok = save_trx(add_tgl, add_jenis, add_kat, add_ket, add_jml, add_uid)
                if ok:
                    st.markdown(f'<div class="success-banner">✅ Transaksi berhasil ditambahkan untuk {html_lib.escape(selected_add_user)}!</div>',
                                unsafe_allow_html=True)

    # ── TAB 4: QR CODE ──
    with adm_tab4:
        st.markdown('<div class="form-title">🔗 Generate QR Code</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card-sub">Buat QR code agar web app bisa diakses dengan scan barcode dari HP</div>',
                    unsafe_allow_html=True)

        qr_url = st.text_input(
            "URL Web App",
            placeholder="https://nama-app.streamlit.app",
            key="qr_url_input",
            help="Masukkan URL deploy Streamlit Cloud atau server Anda",
        )

        if st.button("📱  Generate QR Code", type="primary", key="btn_gen_qr"):
            if not qr_url or not qr_url.startswith("http"):
                st.markdown('<div class="error-banner">⚠️ Masukkan URL yang valid (dimulai dengan http:// atau https://)</div>',
                            unsafe_allow_html=True)
            else:
                with st.spinner("Membuat QR Code..."):
                    qr_bytes = generate_qr_code(qr_url)
                st.session_state["qr_bytes"] = qr_bytes
                st.session_state["qr_url_saved"] = qr_url

        if "qr_bytes" in st.session_state:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="report-title-box">
                <div class="report-title-main">📱 QR Code Siap!</div>
                <div class="report-title-range">{html_lib.escape(st.session_state.get('qr_url_saved', ''))}</div>
            </div>
            """, unsafe_allow_html=True)

            # Tampilkan QR
            qr_image = Image.open(io.BytesIO(st.session_state["qr_bytes"]))
            st.image(qr_image, caption="Scan QR code ini dengan kamera HP", use_container_width=True)

            # Download button
            st.download_button(
                label="⬇️  Download QR Code (PNG)",
                data=st.session_state["qr_bytes"],
                file_name="qrcode_catatan_keuangan.png",
                mime="image/png",
                key="dl_qr",
            )

            st.markdown("""
            <div class="balance-chip">
                💡 <strong>Tips:</strong> Print QR code ini dan tempel di kasir atau meja kerja
            </div>
            """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTING
# ═════════════════════════════════════════════════════════════════════════════
if not st.session_state["logged_in"]:
    show_login_page()
else:
    show_sidebar()
    user = st.session_state["user"]
    if user["role"] == "admin":
        show_admin_dashboard()
    else:
        show_user_dashboard()
