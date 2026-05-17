// pages/Movimientos.jsx
// Responsabilidad: registro de entradas y salidas de stock.
// Trazabilidad: REQ-F02, REQ-F03

import { useState, useEffect } from 'react';
import { repuestosService, entradaStockService, salidaStockService } from '../services/api';

export default function Movimientos() {
  const [tipo, setTipo] = useState('entrada');
  const [repuestos, setRepuestos] = useState([]);
  const [form, setForm] = useState({ repuesto_id: '', cantidad: '', empleado: '', proveedor: '', finalidad: '' });
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    repuestosService.listar().then(setRepuestos).catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje('');
    setError('');
    setLoading(true);
    try {
      const payload = {
        repuesto_id: parseInt(form.repuesto_id, 10),
        cantidad: parseInt(form.cantidad, 10),
        empleado: form.empleado,
        ...(tipo === 'entrada' ? { proveedor: form.proveedor } : { finalidad: form.finalidad }),
      };
      if (tipo === 'entrada') {
        await entradaStockService.registrar(payload);
      } else {
        await salidaStockService.registrar(payload);
      }
      setMensaje(`${tipo === 'entrada' ? 'Entrada' : 'Salida'} registrada correctamente.`);
      setForm({ repuesto_id: '', cantidad: '', empleado: '', proveedor: '', finalidad: '' });
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <h2 style={styles.titulo}>Movimientos de Stock</h2>

      <div style={styles.tabs}>
        {['entrada', 'salida'].map((t) => (
          <button
            key={t}
            style={{ ...styles.tab, ...(tipo === t ? styles.tabActivo : {}) }}
            onClick={() => setTipo(t)}
          >
            {t === 'entrada' ? '📦 Entrada (reposición)' : '🚗 Salida (venta/uso)'}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.field}>
          <label style={styles.label}>Repuesto</label>
          <select
            style={styles.input}
            value={form.repuesto_id}
            onChange={(e) => setForm({ ...form, repuesto_id: e.target.value })}
            required
          >
            <option value="">Seleccionar repuesto...</option>
            {repuestos.map((r) => (
              <option key={r.id} value={r.id}>
                {r.nombre} — {r.categoria} (stock: {r.stock_actual})
              </option>
            ))}
          </select>
        </div>

        <div style={styles.field}>
          <label style={styles.label}>Cantidad</label>
          <input
            style={styles.input}
            type="number"
            min="1"
            value={form.cantidad}
            onChange={(e) => setForm({ ...form, cantidad: e.target.value })}
            required
          />
        </div>

        <div style={styles.field}>
          <label style={styles.label}>Empleado</label>
          <input
            style={styles.input}
            type="text"
            value={form.empleado}
            onChange={(e) => setForm({ ...form, empleado: e.target.value })}
            required
          />
        </div>

        {tipo === 'entrada' ? (
          <div style={styles.field}>
            <label style={styles.label}>Proveedor</label>
            <input
              style={styles.input}
              type="text"
              value={form.proveedor}
              onChange={(e) => setForm({ ...form, proveedor: e.target.value })}
              required
            />
          </div>
        ) : (
          <div style={styles.field}>
            <label style={styles.label}>Finalidad</label>
            <input
              style={styles.input}
              type="text"
              placeholder="venta / uso interno / garantía..."
              value={form.finalidad}
              onChange={(e) => setForm({ ...form, finalidad: e.target.value })}
              required
            />
          </div>
        )}

        {mensaje && <p style={styles.ok}>{mensaje}</p>}
        {error && <p style={styles.error}>⚠ {error}</p>}

        <button style={styles.btn} type="submit" disabled={loading}>
          {loading ? 'Registrando...' : `Registrar ${tipo}`}
        </button>
      </form>
    </div>
  );
}

const styles = {
  page: { padding: '1.5rem', fontFamily: 'system-ui, sans-serif', maxWidth: '600px' },
  titulo: { color: '#1B3A5C', marginBottom: '1.25rem' },
  tabs: { display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' },
  tab: { padding: '0.55rem 1rem', border: '2px solid #1B3A5C', borderRadius: '6px', background: '#fff', cursor: 'pointer', fontWeight: '500' },
  tabActivo: { background: '#1B3A5C', color: '#fff' },
  form: { background: '#fff', border: '1px solid #e2e8f0', borderRadius: '10px', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.3rem' },
  label: { fontSize: '0.85rem', fontWeight: '600', color: '#374151' },
  input: { padding: '0.55rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  btn: { background: '#1B3A5C', color: '#fff', border: 'none', borderRadius: '6px', padding: '0.7rem', fontSize: '1rem', cursor: 'pointer', fontWeight: '600' },
  ok: { color: '#16a34a', fontWeight: '600', margin: 0 },
  error: { color: '#dc2626', margin: 0 },
};
