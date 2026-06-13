// pages/Repuestos.jsx
// Responsabilidad: listado, filtros y registro de repuestos.
// Trazabilidad: REQ-F01, REQ-F04

import { useState, useEffect, useCallback } from 'react';
import { repuestosService } from '../services/api';

const CATEGORIAS = ['', 'auto', 'moto', 'camioneta'];

export default function Repuestos() {
  const [repuestos, setRepuestos] = useState([]);
  const [filtroCategoria, setFiltroCategoria] = useState('');
  const [filtroNombre, setFiltroNombre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mostrarForm, setMostrarForm] = useState(false);
  const [form, setForm] = useState({
    nombre: '', categoria: 'auto', marca: '',
    numero_serie: '', precio: '', stock_inicial: '', stock_minimo: '5',
  });

  const cargarRepuestos = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = {};
      if (filtroCategoria) params.categoria = filtroCategoria;
      if (filtroNombre) params.nombre = filtroNombre;
      const data = await repuestosService.listar(params);
      setRepuestos(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [filtroCategoria, filtroNombre]);

  useEffect(() => { cargarRepuestos(); }, [cargarRepuestos]);

  const handleCrear = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await repuestosService.crear({
        ...form,
        precio: parseFloat(form.precio),
        stock_inicial: parseInt(form.stock_inicial, 10),
        stock_minimo: parseInt(form.stock_minimo, 10),
      });
      setMostrarForm(false);
      setForm({ nombre: '', categoria: 'auto', marca: '', numero_serie: '', precio: '', stock_inicial: '', stock_minimo: '5' });
      cargarRepuestos();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.topBar}>
        <h2 style={styles.titulo}>Repuestos</h2>
        <button style={styles.btnPrimary} onClick={() => setMostrarForm(!mostrarForm)}>
          {mostrarForm ? 'Cancelar' : '+ Nuevo repuesto'}
        </button>
      </div>

      {mostrarForm && (
        <form onSubmit={handleCrear} style={styles.form}>
          <h3 style={{ margin: '0 0 1rem' }}>Registrar repuesto</h3>
          <div style={styles.grid}>
            {[
              ['nombre', 'Nombre', 'text'],
              ['marca', 'Marca', 'text'],
              ['numero_serie', 'Número de serie', 'text'],
              ['precio', 'Precio ($)', 'number'],
              ['stock_inicial', 'Stock inicial', 'number'],
              ['stock_minimo', 'Stock mínimo', 'number'],
            ].map(([key, label, type]) => (
              <div key={key} style={styles.field}>
                <label style={styles.label}>{label}</label>
                <input
                  style={styles.input}
                  type={type}
                  value={form[key]}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  required
                  min={type === 'number' ? '0' : undefined}
                  step={key === 'precio' ? '0.01' : '1'}
                />
              </div>
            ))}
            <div style={styles.field}>
              <label style={styles.label}>Categoría</label>
              <select
                style={styles.input}
                value={form.categoria}
                onChange={(e) => setForm({ ...form, categoria: e.target.value })}
              >
                {CATEGORIAS.filter(Boolean).map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btnPrimary} type="submit">Guardar</button>
        </form>
      )}

      <div style={styles.filtros}>
        <select
          style={styles.select}
          value={filtroCategoria}
          onChange={(e) => setFiltroCategoria(e.target.value)}
        >
          {CATEGORIAS.map((c) => (
            <option key={c} value={c}>{c || 'Todas las categorías'}</option>
          ))}
        </select>
        <input
          style={styles.inputFiltro}
          placeholder="Buscar por nombre..."
          value={filtroNombre}
          onChange={(e) => setFiltroNombre(e.target.value)}
        />
      </div>

      {loading && <p>Cargando...</p>}
      {!loading && repuestos.length === 0 && <p style={{ color: '#64748b' }}>No hay repuestos para mostrar.</p>}

      {!loading && repuestos.length > 0 && (
        <table style={styles.tabla}>
          <thead>
            <tr>
              {['Nombre', 'Categoría', 'Marca', 'N° Serie', 'Precio', 'Stock', 'Mín.'].map((h) => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {repuestos.map((r) => (
              <tr key={r.id} style={r.stock_actual <= r.stock_minimo ? { background: '#fef2f2' } : {}}>
                <td style={styles.td}>{r.nombre}</td>
                <td style={styles.td}>{r.categoria}</td>
                <td style={styles.td}>{r.marca}</td>
                <td style={styles.td}>{r.numero_serie}</td>
                <td style={styles.td}>${r.precio.toLocaleString()}</td>
                <td style={{ ...styles.td, color: r.stock_actual <= r.stock_minimo ? '#dc2626' : 'inherit', fontWeight: r.stock_actual <= r.stock_minimo ? 'bold' : 'normal' }}>
                  {r.stock_actual}
                </td>
                <td style={styles.td}>{r.stock_minimo}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

const styles = {
  page: { padding: '1.5rem', fontFamily: 'system-ui, sans-serif' },
  topBar: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' },
  titulo: { margin: 0, color: '#1B3A5C' },
  form: {
    background: '#fff', border: '1px solid #e2e8f0', borderRadius: '10px',
    padding: '1.5rem', marginBottom: '1.5rem',
  },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.3rem' },
  label: { fontSize: '0.8rem', fontWeight: '600', color: '#374151' },
  input: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  filtros: { display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' },
  select: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  inputFiltro: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem', minWidth: '220px' },
  btnPrimary: {
    background: '#1B3A5C', color: '#fff', border: 'none',
    borderRadius: '6px', padding: '0.55rem 1.1rem', cursor: 'pointer', fontWeight: '600',
  },
  tabla: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: '8px', overflow: 'hidden' },
  th: { background: '#1B3A5C', color: '#fff', padding: '0.65rem 0.85rem', textAlign: 'left', fontSize: '0.875rem' },
  td: { padding: '0.6rem 0.85rem', borderBottom: '1px solid #e2e8f0', fontSize: '0.9rem' },
  error: { color: '#dc2626', fontSize: '0.875rem' },
};
