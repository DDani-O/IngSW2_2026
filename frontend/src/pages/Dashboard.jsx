// pages/Dashboard.jsx
// Responsabilidad: pantalla principal con resumen de inventario y accesos.
// Trazabilidad: REQ-F04, REQ-F05

import { useEffect, useState } from 'react';
import { repuestosService, alertasService } from '../services/api';

export default function Dashboard({ onLogout }) {
  const [totalRepuestos, setTotalRepuestos] = useState(0);
  const [stockCritico, setStockCritico] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cargar = async () => {
      try {
        const [repuestos, criticos] = await Promise.all([
          repuestosService.listar(),
          alertasService.stockCritico(),
        ]);
        setTotalRepuestos(repuestos.length);
        setStockCritico(criticos);
      } catch (e) {
        console.error('Error cargando dashboard:', e);
      } finally {
        setLoading(false);
      }
    };
    cargar();
  }, []);

  return (
    <div style={styles.page}>
      <header style={styles.header}>
        <h1 style={styles.titulo}>🔧 AutoBhan Autopartes</h1>
      </header>

      {loading ? (
        <p style={{ padding: '2rem' }}>Cargando...</p>
      ) : (
        <main style={styles.main}>
          <div style={styles.cards}>
            <div style={styles.card}>
              <span style={styles.cardNum}>{totalRepuestos}</span>
              <span style={styles.cardLabel}>Repuestos registrados</span>
            </div>
            <div style={{ ...styles.card, borderColor: stockCritico.length > 0 ? '#dc2626' : '#16a34a' }}>
              <span style={{ ...styles.cardNum, color: stockCritico.length > 0 ? '#dc2626' : '#16a34a' }}>
                {stockCritico.length}
              </span>
              <span style={styles.cardLabel}>En stock crítico</span>
            </div>
          </div>

          {stockCritico.length > 0 && (
            <div style={styles.alertBox}>
              <h3 style={{ margin: '0 0 0.75rem', color: '#7f1d1d' }}>⚠ Repuestos en stock crítico</h3>
              <table style={styles.tabla}>
                <thead>
                  <tr>
                    {['Nombre', 'Categoría', 'Stock actual', 'Stock mínimo'].map((h) => (
                      <th key={h} style={styles.th}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {stockCritico.map((r) => (
                    <tr key={r.id}>
                      <td style={styles.td}>{r.nombre}</td>
                      <td style={styles.td}>{r.categoria}</td>
                      <td style={{ ...styles.td, color: '#dc2626', fontWeight: 'bold' }}>{r.stock_actual}</td>
                      <td style={styles.td}>{r.stock_minimo}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </main>
      )}
    </div>
  );
}

const styles = {
  page: { minHeight: '100vh', background: '#f0f4f8', fontFamily: 'system-ui, sans-serif' },
  header: {
    background: '#1B3A5C', color: '#fff', padding: '1rem 2rem',
    display: 'flex', alignItems: 'center',
  },
  titulo: { margin: 0, fontSize: '1.25rem' },

  main: { padding: '2rem' },
  cards: { display: 'flex', gap: '1.5rem', marginBottom: '2rem', flexWrap: 'wrap' },
  card: {
    background: '#fff', border: '2px solid #e2e8f0', borderRadius: '10px',
    padding: '1.5rem 2rem', display: 'flex', flexDirection: 'column',
    alignItems: 'center', minWidth: '160px',
  },
  cardNum: { fontSize: '2.5rem', fontWeight: 'bold', color: '#1B3A5C' },
  cardLabel: { fontSize: '0.875rem', color: '#64748b', marginTop: '0.25rem' },
  alertBox: {
    background: '#fef2f2', border: '1px solid #fecaca',
    borderRadius: '10px', padding: '1.25rem',
  },
  tabla: { width: '100%', borderCollapse: 'collapse' },
  th: {
    background: '#fee2e2', padding: '0.5rem 0.75rem',
    textAlign: 'left', fontSize: '0.875rem', color: '#7f1d1d',
  },
  td: { padding: '0.5rem 0.75rem', borderBottom: '1px solid #fecaca', fontSize: '0.9rem' },
};
