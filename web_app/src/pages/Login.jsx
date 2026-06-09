import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { supabase } from '../lib/supabase'
import bcrypt from 'bcryptjs'
import { Wallet, Lock, User, AlertCircle, CheckCircle, UserPlus, LogIn, Eye, EyeOff } from 'lucide-react'

export default function Login({ onLogin }) {
  const [mode, setMode] = useState('login') // 'login' | 'register'

  // --- Login State ---
  const [loginUsername, setLoginUsername] = useState('')
  const [loginPassword, setLoginPassword] = useState('')
  const [showLoginPassword, setShowLoginPassword] = useState(false)
  const [loginError, setLoginError] = useState('')
  const [loginLoading, setLoginLoading] = useState(false)

  // --- Register State ---
  const [regUsername, setRegUsername] = useState('')
  const [regPassword, setRegPassword] = useState('')
  const [regConfirmPassword, setRegConfirmPassword] = useState('')
  const [showRegPassword, setShowRegPassword] = useState(false)
  const [showRegConfirm, setShowRegConfirm] = useState(false)
  const [regError, setRegError] = useState('')
  const [regSuccess, setRegSuccess] = useState('')
  const [regLoading, setRegLoading] = useState(false)

  // --- Handlers ---
  const handleLogin = async (e) => {
    e.preventDefault()
    setLoginError('')
    setLoginLoading(true)

    try {
      const { data, error: dbError } = await supabase
        .from('users')
        .select('*')
        .eq('username', loginUsername.toLowerCase().trim())

      if (dbError) throw dbError

      if (!data || data.length === 0) {
        setLoginError('Username tidak ditemukan!')
        setLoginLoading(false)
        return
      }

      const user = data[0]
      const isValid = bcrypt.compareSync(loginPassword, user.password)

      if (!isValid) {
        setLoginError('Password salah!')
        setLoginLoading(false)
        return
      }

      const { password: _, ...userWithoutPassword } = user
      onLogin(userWithoutPassword)
    } catch (err) {
      setLoginError(err.message || 'Terjadi kesalahan sistem')
    } finally {
      setLoginLoading(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setRegError('')
    setRegSuccess('')

    const usernameClean = regUsername.toLowerCase().trim()

    // --- Validasi Sisi Client ---
    if (usernameClean.length < 3) {
      setRegError('Username minimal 3 karakter.')
      return
    }
    if (!/^[a-z0-9_]+$/.test(usernameClean)) {
      setRegError('Username hanya boleh mengandung huruf kecil, angka, dan underscore (_).')
      return
    }
    if (regPassword.length < 6) {
      setRegError('Password minimal 6 karakter.')
      return
    }
    if (regPassword !== regConfirmPassword) {
      setRegError('Konfirmasi password tidak cocok!')
      return
    }

    setRegLoading(true)

    try {
      // --- Validasi Username Unik ke Database ---
      const { data: existingUsers, error: checkError } = await supabase
        .from('users')
        .select('id')
        .eq('username', usernameClean)

      if (checkError) throw checkError

      if (existingUsers && existingUsers.length > 0) {
        setRegError(`Username "${usernameClean}" sudah digunakan. Silakan pilih username lain.`)
        setRegLoading(false)
        return
      }

      // --- Hash Password ---
      const saltRounds = 10
      const hashedPassword = bcrypt.hashSync(regPassword, saltRounds)

      // --- Simpan User Baru ke Database ---
      const { data: newUser, error: insertError } = await supabase
        .from('users')
        .insert({
          username: usernameClean,
          password: hashedPassword,
          role: 'user'
        })
        .select('id, username, role, created_at')
        .single()

      if (insertError) throw insertError

      setRegSuccess(`Akun "${usernameClean}" berhasil dibuat! Silakan login.`)
      setRegUsername('')
      setRegPassword('')
      setRegConfirmPassword('')

      // Auto-switch ke login setelah 2 detik
      setTimeout(() => {
        setMode('login')
        setLoginUsername(usernameClean)
        setRegSuccess('')
      }, 2000)

    } catch (err) {
      setRegError(err.message || 'Terjadi kesalahan saat mendaftar.')
    } finally {
      setRegLoading(false)
    }
  }

  const switchMode = (newMode) => {
    setMode(newMode)
    setLoginError('')
    setRegError('')
    setRegSuccess('')
  }

  // --- Kekuatan Password ---
  const getPasswordStrength = (pw) => {
    if (!pw) return null
    if (pw.length < 6) return { label: 'Terlalu pendek', color: '#ef4444', width: '20%' }
    if (pw.length < 8) return { label: 'Lemah', color: '#f59e0b', width: '40%' }
    const hasUpper = /[A-Z]/.test(pw)
    const hasNumber = /[0-9]/.test(pw)
    const hasSpecial = /[^a-zA-Z0-9]/.test(pw)
    const score = [hasUpper, hasNumber, hasSpecial].filter(Boolean).length
    if (score === 0) return { label: 'Sedang', color: '#f59e0b', width: '55%' }
    if (score === 1) return { label: 'Kuat', color: '#10b981', width: '75%' }
    return { label: 'Sangat Kuat', color: '#6366f1', width: '100%' }
  }

  const pwStrength = getPasswordStrength(regPassword)

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', padding: '20px' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="glass-panel"
        style={{ width: '100%', maxWidth: '420px', padding: '40px 30px', overflow: 'hidden' }}
      >
        {/* Logo & Judul */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ repeat: Infinity, duration: 3, ease: 'easeInOut' }}
            style={{ display: 'inline-block', marginBottom: '15px' }}
          >
            <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent-color), #8b5cf6)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 10px 25px rgba(99, 102, 241, 0.4)', margin: '0 auto' }}>
              <Wallet color="white" size={32} />
            </div>
          </motion.div>
          <h1 style={{ fontSize: '24px', fontWeight: '800', margin: '0 0 5px 0' }}>Catatan Keuangan</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', margin: 0 }}>
            {mode === 'login' ? 'Masuk ke akun Anda' : 'Buat akun baru'}
          </p>
        </div>

        {/* Tab Toggle */}
        <div style={{ display: 'flex', gap: '4px', background: 'rgba(255,255,255,0.05)', padding: '4px', borderRadius: '12px', marginBottom: '28px' }}>
          <button
            id="tab-login"
            type="button"
            onClick={() => switchMode('login')}
            className={`btn ${mode === 'login' ? 'btn-primary' : 'btn-ghost'}`}
            style={{ flex: 1, padding: '9px', fontSize: '13px' }}
          >
            <LogIn size={15} /> Masuk
          </button>
          <button
            id="tab-register"
            type="button"
            onClick={() => switchMode('register')}
            className={`btn ${mode === 'register' ? 'btn-primary' : 'btn-ghost'}`}
            style={{ flex: 1, padding: '9px', fontSize: '13px' }}
          >
            <UserPlus size={15} /> Daftar
          </button>
        </div>

        {/* ===== FORM LOGIN ===== */}
        <AnimatePresence mode="wait">
          {mode === 'login' && (
            <motion.div
              key="login-form"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.25 }}
            >
              {loginError && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', padding: '12px', borderRadius: '10px', color: 'var(--danger)', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}
                >
                  <AlertCircle size={16} />
                  {loginError}
                </motion.div>
              )}

              <form onSubmit={handleLogin}>
                <div style={{ marginBottom: '18px' }}>
                  <label className="input-label">Username</label>
                  <div style={{ position: 'relative' }}>
                    <User size={17} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                    <input
                      id="login-username"
                      type="text"
                      className="input-field"
                      style={{ paddingLeft: '42px' }}
                      placeholder="Masukkan username"
                      value={loginUsername}
                      onChange={(e) => setLoginUsername(e.target.value)}
                      autoComplete="username"
                      required
                    />
                  </div>
                </div>

                <div style={{ marginBottom: '28px' }}>
                  <label className="input-label">Password</label>
                  <div style={{ position: 'relative' }}>
                    <Lock size={17} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                    <input
                      id="login-password"
                      type={showLoginPassword ? 'text' : 'password'}
                      className="input-field"
                      style={{ paddingLeft: '42px', paddingRight: '42px' }}
                      placeholder="Masukkan password"
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      autoComplete="current-password"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowLoginPassword(!showLoginPassword)}
                      style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', padding: '4px', display: 'flex' }}
                    >
                      {showLoginPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                    </button>
                  </div>
                </div>

                <button
                  id="btn-login-submit"
                  type="submit"
                  className="btn btn-primary"
                  style={{ width: '100%', padding: '13px', fontSize: '15px' }}
                  disabled={loginLoading}
                >
                  {loginLoading ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}>
                      <span className="spinner" />
                      Memproses...
                    </span>
                  ) : (
                    <>
                      <LogIn size={17} /> Masuk ke Dashboard
                    </>
                  )}
                </button>
              </form>

              <div style={{ marginTop: '20px', textAlign: 'center', fontSize: '13px', color: 'var(--text-secondary)' }}>
                Belum punya akun?{' '}
                <button
                  type="button"
                  onClick={() => switchMode('register')}
                  style={{ background: 'none', border: 'none', color: 'var(--accent-color)', fontWeight: '600', cursor: 'pointer', fontSize: '13px', fontFamily: 'var(--font-family)', padding: 0 }}
                >
                  Daftar sekarang
                </button>
              </div>
            </motion.div>
          )}

          {/* ===== FORM REGISTER ===== */}
          {mode === 'register' && (
            <motion.div
              key="register-form"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.25 }}
            >
              {/* Pesan Error */}
              {regError && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', padding: '12px', borderRadius: '10px', color: 'var(--danger)', fontSize: '13px', display: 'flex', alignItems: 'flex-start', gap: '8px', marginBottom: '16px' }}
                >
                  <AlertCircle size={16} style={{ marginTop: '1px', flexShrink: 0 }} />
                  {regError}
                </motion.div>
              )}

              {/* Pesan Sukses */}
              {regSuccess && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  style={{ background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.3)', padding: '12px', borderRadius: '10px', color: 'var(--success)', fontSize: '13px', display: 'flex', alignItems: 'flex-start', gap: '8px', marginBottom: '16px' }}
                >
                  <CheckCircle size={16} style={{ marginTop: '1px', flexShrink: 0 }} />
                  {regSuccess}
                </motion.div>
              )}

              <form onSubmit={handleRegister}>
                {/* Username */}
                <div style={{ marginBottom: '16px' }}>
                  <label className="input-label">Username</label>
                  <div style={{ position: 'relative' }}>
                    <User size={17} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                    <input
                      id="reg-username"
                      type="text"
                      className="input-field"
                      style={{ paddingLeft: '42px' }}
                      placeholder="min. 3 karakter (a-z, 0-9, _)"
                      value={regUsername}
                      onChange={(e) => setRegUsername(e.target.value)}
                      autoComplete="username"
                      required
                    />
                  </div>
                  <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginTop: '5px', marginLeft: '2px' }}>
                    Hanya huruf kecil, angka, dan underscore. Contoh: <em>budi_01</em>
                  </p>
                </div>

                {/* Password */}
                <div style={{ marginBottom: '16px' }}>
                  <label className="input-label">Password</label>
                  <div style={{ position: 'relative' }}>
                    <Lock size={17} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                    <input
                      id="reg-password"
                      type={showRegPassword ? 'text' : 'password'}
                      className="input-field"
                      style={{ paddingLeft: '42px', paddingRight: '42px' }}
                      placeholder="min. 6 karakter"
                      value={regPassword}
                      onChange={(e) => setRegPassword(e.target.value)}
                      autoComplete="new-password"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowRegPassword(!showRegPassword)}
                      style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', padding: '4px', display: 'flex' }}
                    >
                      {showRegPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                    </button>
                  </div>
                  {/* Indikator Kekuatan Password */}
                  {pwStrength && (
                    <div style={{ marginTop: '8px' }}>
                      <div style={{ height: '4px', borderRadius: '4px', background: 'rgba(255,255,255,0.1)', overflow: 'hidden' }}>
                        <motion.div
                          initial={{ width: '0%' }}
                          animate={{ width: pwStrength.width }}
                          transition={{ duration: 0.3 }}
                          style={{ height: '100%', borderRadius: '4px', background: pwStrength.color }}
                        />
                      </div>
                      <p style={{ fontSize: '11px', color: pwStrength.color, marginTop: '4px', fontWeight: '600' }}>
                        {pwStrength.label}
                      </p>
                    </div>
                  )}
                </div>

                {/* Konfirmasi Password */}
                <div style={{ marginBottom: '24px' }}>
                  <label className="input-label">Konfirmasi Password</label>
                  <div style={{ position: 'relative' }}>
                    <Lock size={17} style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-secondary)' }} />
                    <input
                      id="reg-confirm-password"
                      type={showRegConfirm ? 'text' : 'password'}
                      className="input-field"
                      style={{
                        paddingLeft: '42px',
                        paddingRight: '42px',
                        borderColor: regConfirmPassword && regPassword !== regConfirmPassword
                          ? 'rgba(239,68,68,0.5)'
                          : regConfirmPassword && regPassword === regConfirmPassword
                          ? 'rgba(16,185,129,0.5)'
                          : undefined
                      }}
                      placeholder="Ulangi password Anda"
                      value={regConfirmPassword}
                      onChange={(e) => setRegConfirmPassword(e.target.value)}
                      autoComplete="new-password"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowRegConfirm(!showRegConfirm)}
                      style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', padding: '4px', display: 'flex' }}
                    >
                      {showRegConfirm ? <EyeOff size={17} /> : <Eye size={17} />}
                    </button>
                  </div>
                  {regConfirmPassword && regPassword === regConfirmPassword && (
                    <p style={{ fontSize: '11px', color: 'var(--success)', marginTop: '5px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <CheckCircle size={11} /> Password cocok
                    </p>
                  )}
                  {regConfirmPassword && regPassword !== regConfirmPassword && (
                    <p style={{ fontSize: '11px', color: 'var(--danger)', marginTop: '5px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <AlertCircle size={11} /> Password tidak cocok
                    </p>
                  )}
                </div>

                <button
                  id="btn-register-submit"
                  type="submit"
                  className="btn btn-primary"
                  style={{ width: '100%', padding: '13px', fontSize: '15px' }}
                  disabled={regLoading}
                >
                  {regLoading ? (
                    <span style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'center' }}>
                      <span className="spinner" />
                      Mendaftarkan...
                    </span>
                  ) : (
                    <>
                      <UserPlus size={17} /> Buat Akun
                    </>
                  )}
                </button>
              </form>

              <div style={{ marginTop: '20px', textAlign: 'center', fontSize: '13px', color: 'var(--text-secondary)' }}>
                Sudah punya akun?{' '}
                <button
                  type="button"
                  onClick={() => switchMode('login')}
                  style={{ background: 'none', border: 'none', color: 'var(--accent-color)', fontWeight: '600', cursor: 'pointer', fontSize: '13px', fontFamily: 'var(--font-family)', padding: 0 }}
                >
                  Masuk sekarang
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '11px', color: 'var(--text-secondary)', opacity: 0.7 }}>
          <p>🔒 Data terenkripsi · Sistem Keamanan Tinggi</p>
        </div>
      </motion.div>
    </div>
  )
}
