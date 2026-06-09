import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { supabase } from '../lib/supabase'
import { LogOut, Home, BarChart2, History } from 'lucide-react'
import TabDashboard from '../components/TabDashboard'
import TabAnalisis from '../components/TabAnalisis'
import TabRiwayat from '../components/TabRiwayat'

export default function Dashboard({ session, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const fetchTransactions = async () => {
    try {
      const { data, error } = await supabase
        .from('transaksi')
        .select('*')
        .eq('user_id', session.id)
        .order('tanggal', { ascending: false })
        .order('created_at', { ascending: false })
      
      if (error) throw error
      setTransactions(data || [])
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchTransactions()
  }, [])

  const handleSubmit = async (formData) => {
    setIsSubmitting(true)
    try {
      const { error } = await supabase.from('transaksi').insert({
        ...formData,
        jumlah: parseFloat(formData.jumlah),
        user_id: session.id
      })
      if (error) throw error
      fetchTransactions()
    } catch (err) {
      alert('Gagal menyimpan transaksi: ' + err.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Hapus transaksi ini?')) return
    try {
      const { error } = await supabase.from('transaksi').delete().eq('id', id)
      if (error) throw error
      fetchTransactions()
    } catch (err) {
      alert('Gagal menghapus: ' + err.message)
    }
  }

  const formatRp = (num) => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(num)

  const totalIncome = transactions.filter(t => t.jenis === 'pemasukan').reduce((sum, t) => sum + parseFloat(t.jumlah), 0)
  const totalExpense = transactions.filter(t => t.jenis === 'pengeluaran').reduce((sum, t) => sum + parseFloat(t.jumlah), 0)
  const balance = totalIncome - totalExpense

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', padding: '20px 0' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: '800', margin: '0 0 5px 0' }}>Halo, {session.username} 👋</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '14px', margin: 0 }}>Kelola keuangan Anda dengan mudah</p>
        </div>
        <button onClick={onLogout} className="btn btn-ghost" style={{ padding: '8px 14px' }}>
          <LogOut size={16} /> <span className="hidden-mobile">Keluar</span>
        </button>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '5px', background: 'rgba(255,255,255,0.05)', padding: '5px', borderRadius: '12px', marginBottom: '24px', overflowX: 'auto' }}>
        <button 
          className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-ghost'}`} 
          onClick={() => setActiveTab('dashboard')}
          style={{ flex: 1, padding: '10px' }}
        >
          <Home size={16} /> Dashboard
        </button>
        <button 
          className={`btn ${activeTab === 'analisis' ? 'btn-primary' : 'btn-ghost'}`} 
          onClick={() => setActiveTab('analisis')}
          style={{ flex: 1, padding: '10px' }}
        >
          <BarChart2 size={16} /> Analisis
        </button>
        <button 
          className={`btn ${activeTab === 'riwayat' ? 'btn-primary' : 'btn-ghost'}`} 
          onClick={() => setActiveTab('riwayat')}
          style={{ flex: 1, padding: '10px' }}
        >
          <History size={16} /> Riwayat
        </button>
      </div>

      {/* Tab Content */}
      <div style={{ minHeight: '500px' }}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px', color: 'var(--text-secondary)' }}>Memuat data...</div>
        ) : (
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && (
              <TabDashboard key="dashboard" transactions={transactions} balance={balance} totalIncome={totalIncome} totalExpense={totalExpense} formatRp={formatRp} onSubmitTransaction={handleSubmit} isSubmitting={isSubmitting} />
            )}
            {activeTab === 'analisis' && (
              <TabAnalisis key="analisis" transactions={transactions} formatRp={formatRp} />
            )}
            {activeTab === 'riwayat' && (
              <TabRiwayat key="riwayat" transactions={transactions} formatRp={formatRp} onDelete={handleDelete} />
            )}
          </AnimatePresence>
        )}
      </div>
    </div>
  )
}
