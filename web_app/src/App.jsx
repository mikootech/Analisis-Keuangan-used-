import React, { useState, useEffect } from 'react'
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import './index.css'

function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Memeriksa session dari localStorage (custom auth karena tidak menggunakan Supabase Auth bawaan)
    const storedUser = localStorage.getItem('user_session')
    if (storedUser) {
      try {
        setSession(JSON.parse(storedUser))
      } catch (e) {
        localStorage.removeItem('user_session')
      }
    }
    setLoading(false)
  }, [])

  const handleLogin = (userData) => {
    setSession(userData)
    localStorage.setItem('user_session', JSON.stringify(userData))
  }

  const handleLogout = () => {
    setSession(null)
    localStorage.removeItem('user_session')
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', color: 'white' }}>
        <div className="animate-fade-in">Memuat...</div>
      </div>
    )
  }

  return (
    <Routes>
      <Route path="/" element={session ? <Dashboard session={session} onLogout={handleLogout} /> : <Navigate to="/login" replace />} />
      <Route path="/login" element={!session ? <Login onLogin={handleLogin} /> : <Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
