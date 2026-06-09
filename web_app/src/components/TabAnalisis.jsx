import React, { useMemo } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { Activity } from 'lucide-react'

export default function TabAnalisis({ transactions, formatRp }) {
  const data = useMemo(() => {
    // Kelompokkan berdasarkan tanggal untuk LineChart
    const grouped = {}
    transactions.forEach(t => {
      const date = t.tanggal
      if (!grouped[date]) {
        grouped[date] = { name: new Date(date).toLocaleDateString('id-ID', { month: 'short', day: 'numeric' }), pemasukan: 0, pengeluaran: 0 }
      }
      if (t.jenis === 'pemasukan') grouped[date].pemasukan += parseFloat(t.jumlah)
      else grouped[date].pengeluaran += parseFloat(t.jumlah)
    })
    
    // Sort berdasarkan tanggal lama ke baru
    return Object.keys(grouped).sort().map(k => grouped[k]).slice(-7) // Ambil 7 hari terakhir
  }, [transactions])

  const pieData = useMemo(() => {
    let warung = 0
    let pribadi = 0
    transactions.filter(t => t.jenis === 'pengeluaran').forEach(t => {
      if (t.kategori === 'warung') warung += parseFloat(t.jumlah)
      else pribadi += parseFloat(t.jumlah)
    })
    const total = warung + pribadi
    const wPct = total === 0 ? 0 : Math.round((warung/total)*100)
    const pPct = total === 0 ? 0 : Math.round((pribadi/total)*100)
    
    return [
      { name: `Warung (${wPct}%)`, value: warung },
      { name: `Pribadi (${pPct}%)`, value: pribadi }
    ]
  }, [transactions])

  const COLORS = ['#f59e0b', '#6366f1'] // Amber untuk Warung, Indigo untuk Pribadi

  if (transactions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-secondary)' }}>
        Belum ada data untuk dianalisis.
      </div>
    )
  }

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      <div className="glass-panel" style={{ padding: '24px', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={18} /> Tren Pemasukan & Pengeluaran (7 Hari Terakhir)
        </h2>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart data={data} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
              <XAxis dataKey="name" stroke="var(--text-secondary)" fontSize={12} tickMargin={10} />
              <YAxis stroke="var(--text-secondary)" fontSize={12} tickFormatter={(val) => `Rp${val/1000}k`} tickMargin={10} />
              <Tooltip 
                contentStyle={{ backgroundColor: 'var(--bg-color)', border: '1px solid var(--surface-border)', borderRadius: '10px', color: 'var(--text-primary)', boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }}
                formatter={(value) => formatRp(value)}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Line type="monotone" dataKey="pemasukan" name="Pemasukan" stroke="var(--success)" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
              <Line type="monotone" dataKey="pengeluaran" name="Pengeluaran" stroke="var(--danger)" strokeWidth={3} dot={{ r: 4, strokeWidth: 2 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2 style={{ fontSize: '16px', fontWeight: '700', marginBottom: '20px' }}>Distribusi Pengeluaran</h2>
        <div style={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="45%"
                innerRadius={70}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
                stroke="none"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => formatRp(value)} contentStyle={{ backgroundColor: 'var(--bg-color)', border: '1px solid var(--surface-border)', borderRadius: '10px', boxShadow: '0 4px 20px rgba(0,0,0,0.3)' }} />
              <Legend verticalAlign="bottom" height={36} wrapperStyle={{ paddingTop: '20px' }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </motion.div>
  )
}
