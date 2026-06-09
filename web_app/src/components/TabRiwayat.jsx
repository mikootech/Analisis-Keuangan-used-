import React, { useState, useMemo } from 'react'
import { motion } from 'framer-motion'
import { Filter, Trash2, Download } from 'lucide-react'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export default function TabRiwayat({ transactions, formatRp, onDelete }) {
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const filteredTransactions = useMemo(() => {
    return transactions.filter(t => {
      const dateStr = t.tanggal
      if (startDate && dateStr < startDate) return false
      if (endDate && dateStr > endDate) return false
      return true
    })
  }, [transactions, startDate, endDate])

  const exportPDF = () => {
    if (filteredTransactions.length === 0) {
      alert("Tidak ada data untuk diekspor pada rentang tanggal ini.")
      return
    }

    const doc = new jsPDF()
    
    // Header PDF
    doc.setFontSize(18)
    doc.text("Laporan Riwayat Transaksi", 14, 22)
    
    doc.setFontSize(11)
    doc.text(`Tanggal Export: ${new Date().toLocaleDateString('id-ID')}`, 14, 30)
    
    let subtitle = "Rentang: Semua Waktu"
    if (startDate && endDate) subtitle = `Rentang: ${startDate} s/d ${endDate}`
    else if (startDate) subtitle = `Rentang: Mulai ${startDate}`
    else if (endDate) subtitle = `Rentang: Sampai ${endDate}`
    doc.text(subtitle, 14, 36)

    // Siapkan data untuk tabel
    const tableColumn = ["Tanggal", "Jenis", "Kategori", "Keterangan", "Jumlah (Rp)"]
    const tableRows = []

    let totalMasuk = 0
    let totalKeluar = 0

    filteredTransactions.forEach(t => {
      const rowData = [
        new Date(t.tanggal).toLocaleDateString('id-ID'),
        t.jenis === 'pemasukan' ? 'Pemasukan' : 'Pengeluaran',
        t.kategori,
        t.keterangan || '-',
        new Intl.NumberFormat('id-ID').format(t.jumlah)
      ]
      tableRows.push(rowData)

      if (t.jenis === 'pemasukan') totalMasuk += parseFloat(t.jumlah)
      else totalKeluar += parseFloat(t.jumlah)
    })

    autoTable(doc, {
      head: [tableColumn],
      body: tableRows,
      startY: 42,
      theme: 'grid',
      headStyles: { fillColor: [99, 102, 241] }, // warna indigo
      styles: { fontSize: 10 }
    })

    // Summary di bawah tabel
    const finalY = doc.lastAutoTable.finalY || 42
    doc.text(`Total Pemasukan: Rp ${new Intl.NumberFormat('id-ID').format(totalMasuk)}`, 14, finalY + 10)
    doc.text(`Total Pengeluaran: Rp ${new Intl.NumberFormat('id-ID').format(totalKeluar)}`, 14, finalY + 18)
    const profit = totalMasuk - totalKeluar
    doc.text(`Saldo: Rp ${new Intl.NumberFormat('id-ID').format(profit)}`, 14, finalY + 26)

    doc.save(`Laporan_Transaksi_${new Date().getTime()}.pdf`)
  }

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.3 }}>
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', gap: '15px' }}>
          <h2 style={{ fontSize: '16px', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
            <Filter size={18} /> Riwayat Transaksi
          </h2>
          
          <button onClick={exportPDF} className="btn btn-primary" style={{ padding: '8px 16px', fontSize: '13px' }}>
            <Download size={16} /> Export PDF
          </button>
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: '15px', marginBottom: '20px', flexWrap: 'wrap', background: 'rgba(255,255,255,0.02)', padding: '15px', borderRadius: '12px', border: '1px solid var(--surface-border)' }}>
          <div>
            <label className="input-label" style={{ fontSize: '11px' }}>Mulai Tanggal</label>
            <input type="date" className="input-field" style={{ padding: '8px 12px' }} value={startDate} onChange={e => setStartDate(e.target.value)} />
          </div>
          <div>
            <label className="input-label" style={{ fontSize: '11px' }}>Sampai Tanggal</label>
            <input type="date" className="input-field" style={{ padding: '8px 12px' }} value={endDate} onChange={e => setEndDate(e.target.value)} />
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-end' }}>
            <button className="btn btn-ghost" onClick={() => { setStartDate(''); setEndDate(''); }} style={{ padding: '8px 12px', fontSize: '12px' }}>Reset</button>
          </div>
        </div>

        {/* List */}
        {filteredTransactions.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px dashed var(--surface-border)' }}>
            Data tidak ditemukan pada rentang tanggal ini.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {filteredTransactions.map((t) => (
              <motion.div 
                key={t.id}
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ scale: 1.005 }}
                style={{ 
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
                  padding: '14px', borderRadius: '12px', 
                  background: 'rgba(255, 255, 255, 0.03)',
                  borderLeft: `4px solid ${t.jenis === 'pemasukan' ? 'var(--success)' : 'var(--danger)'}`,
                  borderTop: '1px solid var(--surface-border)',
                  borderRight: '1px solid var(--surface-border)',
                  borderBottom: '1px solid var(--surface-border)',
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>{t.keterangan || (t.jenis === 'pemasukan' ? 'Pemasukan' : 'Pengeluaran')}</div>
                  <div style={{ display: 'flex', gap: '10px', fontSize: '11px', color: 'var(--text-secondary)' }}>
                    <span>{new Date(t.tanggal).toLocaleDateString('id-ID')}</span>
                    <span style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px', textTransform: 'capitalize' }}>{t.kategori}</span>
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '14px', fontWeight: '700', color: t.jenis === 'pemasukan' ? 'var(--success)' : 'var(--danger)' }}>
                    {t.jenis === 'pemasukan' ? '+' : '-'}{formatRp(t.jumlah)}
                  </div>
                  <button onClick={() => onDelete(t.id)} style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', marginTop: '4px', opacity: 0.7, transition: 'all 0.2s' }} onMouseOver={e => e.currentTarget.style.color = 'var(--danger)'} onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}>
                    <Trash2 size={14} />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  )
}
