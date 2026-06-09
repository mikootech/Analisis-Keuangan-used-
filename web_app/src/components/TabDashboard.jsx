import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowUpRight, ArrowDownRight, TrendingUp, Plus } from 'lucide-react'

export default function TabDashboard({ transactions, balance, totalIncome, totalExpense, formatRp, onSubmitTransaction, isSubmitting }) {
  const [formData, setFormData] = useState({
    tanggal: new Date().toISOString().split('T')[0],
    jenis: 'pemasukan',
    kategori: 'warung',
    jumlah: '',
    keterangan: ''
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmitTransaction(formData)
    setFormData({ ...formData, jumlah: '', keterangan: '' })
  }

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      {/* Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '30px' }}>
        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid var(--accent-color)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px', color: 'var(--text-secondary)' }}>
            <TrendingUp size={18} color="var(--accent-color)" /> <span style={{ fontSize: '13px', fontWeight: '600' }}>TOTAL SALDO</span>
          </div>
          <div style={{ fontSize: '28px', fontWeight: '800' }}>{formatRp(balance)}</div>
        </div>
        
        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid var(--success)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px', color: 'var(--text-secondary)' }}>
            <ArrowDownRight size={18} color="var(--success)" /> <span style={{ fontSize: '13px', fontWeight: '600' }}>PEMASUKAN</span>
          </div>
          <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--success)' }}>{formatRp(totalIncome)}</div>
        </div>

        <div className="glass-panel" style={{ padding: '20px', borderLeft: '4px solid var(--danger)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px', color: 'var(--text-secondary)' }}>
            <ArrowUpRight size={18} color="var(--danger)" /> <span style={{ fontSize: '13px', fontWeight: '600' }}>PENGELUARAN</span>
          </div>
          <div style={{ fontSize: '22px', fontWeight: '800', color: 'var(--danger)' }}>{formatRp(totalExpense)}</div>
        </div>
      </div>

      {/* Form Tambah Transaksi */}
      <div className="glass-panel" style={{ padding: '24px', maxWidth: '600px', margin: '0 auto' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={18} /> Tambah Transaksi Cepat
        </h2>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', marginBottom: '15px' }}>
            <div style={{ flex: '1 1 200px' }}>
              <label className="input-label">Tanggal</label>
              <input type="date" className="input-field" value={formData.tanggal} onChange={e => setFormData({...formData, tanggal: e.target.value})} required />
            </div>
            <div style={{ flex: '1 1 200px' }}>
              <label className="input-label">Jenis</label>
              <div style={{ display: 'flex', gap: '10px' }}>
                <div 
                  onClick={() => setFormData({...formData, jenis: 'pemasukan'})}
                  style={{ flex: 1, textAlign: 'center', padding: '10px', borderRadius: '8px', cursor: 'pointer', border: formData.jenis === 'pemasukan' ? '1px solid var(--success)' : '1px solid var(--surface-border)', background: formData.jenis === 'pemasukan' ? 'rgba(16, 185, 129, 0.1)' : 'transparent', color: formData.jenis === 'pemasukan' ? 'var(--success)' : 'var(--text-secondary)', fontWeight: '600', fontSize: '13px', transition: 'all 0.2s' }}
                >
                  Pemasukan
                </div>
                <div 
                  onClick={() => setFormData({...formData, jenis: 'pengeluaran'})}
                  style={{ flex: 1, textAlign: 'center', padding: '10px', borderRadius: '8px', cursor: 'pointer', border: formData.jenis === 'pengeluaran' ? '1px solid var(--danger)' : '1px solid var(--surface-border)', background: formData.jenis === 'pengeluaran' ? 'rgba(239, 68, 68, 0.1)' : 'transparent', color: formData.jenis === 'pengeluaran' ? 'var(--danger)' : 'var(--text-secondary)', fontWeight: '600', fontSize: '13px', transition: 'all 0.2s' }}
                >
                  Pengeluaran
                </div>
              </div>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap', marginBottom: '15px' }}>
            <div style={{ flex: '1 1 200px' }}>
              <label className="input-label">Kategori</label>
              <select className="input-field" value={formData.kategori} onChange={e => setFormData({...formData, kategori: e.target.value})}>
                <option value="warung">Warung</option>
                <option value="pribadi">Pribadi</option>
              </select>
            </div>
            <div style={{ flex: '1 1 200px' }}>
              <label className="input-label">Jumlah (Rp)</label>
              <input type="number" className="input-field" value={formData.jumlah} onChange={e => setFormData({...formData, jumlah: e.target.value})} placeholder="Contoh: 50000" required min="1" />
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label className="input-label">Keterangan (opsional)</label>
            <input type="text" className="input-field" value={formData.keterangan} onChange={e => setFormData({...formData, keterangan: e.target.value})} placeholder="Contoh: Beli sabun" />
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={isSubmitting}>
            {isSubmitting ? 'Menyimpan...' : 'Simpan Transaksi'}
          </button>
        </form>
      </div>
    </motion.div>
  )
}
