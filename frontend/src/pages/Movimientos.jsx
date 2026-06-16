// pages/Movimientos.jsx
// Responsabilidad: registro de entradas y salidas de stock.
// Trazabilidad: REQ-F02, REQ-F03

import { useState, useEffect, useRef } from 'react';
import { repuestosService, entradaStockService, salidaStockService } from '../services/api';

export default function Movimientos() {
  const [tipo, setTipo] = useState('entrada');
  const [repuestos, setRepuestos] = useState([]);
  const [form, setForm] = useState({
    repuesto_id: '', cantidad: '', empleado: '', proveedor: '', finalidad: '',
  });
  const [mensaje, setMensaje] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Búsqueda predictiva de repuesto
  const [busqueda, setBusqueda] = useState('');
  const [mostrarLista, setMostrarLista] = useState(false);
  const busquedaRef = useRef(null);
  const listaRef = useRef(null);

  useEffect(() => {
    repuestosService.listar().then(setRepuestos).catch(console.error);
  }, []);

  // Cerrar lista al hacer click fuera
  useEffect(() => {
    const handleClickFuera = (e) => {
      if (
        busquedaRef.current && !busquedaRef.current.contains(e.target) &&
        listaRef.current && !listaRef.current.contains(e.target)
      ) {
        setMostrarLista(false);
      }
    };
    document.addEventListener('mousedown', handleClickFuera);
    return () => document.removeEventListener('mousedown', handleClickFuera);
  }, []);

  const repuestosFiltrados = repuestos.filter((r) => {
    const texto = busqueda.toLowerCase();
    return (
      r.nombre.toLowerCase().includes(texto) ||
      r.categoria.toLowerCase().includes(texto) ||
      r.marca.toLowerCase().includes(texto) ||
      r.numero_serie.toLowerCase().includes(texto)
    );
  }).slice(0, 20);

  const seleccionarRepuesto = (r) => {
    setForm({ ...form, repuesto_id: String(r.id) });
    setBusqueda(`${r.nombre} — ${r.categoria} (stock: ${r.stock_actual})`);
    setMostrarLista(false);
  };

  const repuestoSeleccionado = repuestos.find((r) => String(r.id) === form.repuesto_id);

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
      setBusqueda('');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const limpiarFormulario = () => {
    setForm({ repuesto_id: '', cantidad: '', empleado: '', proveedor: '', finalidad: '' });
    setBusqueda('');
    setMensaje('');
    setError('');
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

        {/* ── Selector de repuesto con búsqueda predictiva ── */}
        <div style={styles.field}>
          <label style={styles.label}>Repuesto</label>
          <div style={styles.autocompleteWrapper}>
            <input
              ref={busquedaRef}
              style={styles.input}
              type="text"
              placeholder="Buscar por nombre, categoría, marca o serie..."
              value={busqueda}
              onChange={(e) => {
                setBusqueda(e.target.value);
                setForm({ ...form, repuesto_id: '' });
                setMostrarLista(true);
              }}
              onFocus={() => setMostrarLista(true)}
              autoComplete="off"
            />
            {mostrarLista && busqueda.length > 0 && (
              <ul ref={listaRef} style={styles.lista}>
                {repuestosFiltrados.length > 0 ? (
                  repuestosFiltrados.map((r) => (
                    <li
                      key={r.id}
                      style={styles.listaItem}
                      onMouseDown={() => seleccionarRepuesto(r)}
                      onMouseEnter={(e) => e.currentTarget.style.background = '#EFF6FF'}
                      onMouseLeave={(e) => e.currentTarget.style.background = '#fff'}
                    >
                      <span style={styles.listaItemNombre}>{r.nombre}</span>
                      <span style={styles.listaItemMeta}>
                        {r.categoria} · {r.marca} · Serie: {r.numero_serie} · Stock: {r.stock_actual}
                      </span>
                    </li>
                  ))
                ) : (
                  <li style={{ ...styles.listaItem, color: '#9ca3af', fontStyle: 'italic' }}>
                    Sin resultados para "{busqueda}"
                  </li>
                )}
              </ul>
            )}
          </div>
          {/* Campo oculto para validación del formulario */}
          <input
            type="hidden"
            value={form.repuesto_id}
            required
          />
          {form.repuesto_id && repuestoSeleccionado && (
            <span style={styles.repuestoConfirmado}>
              ✓ {repuestoSeleccionado.nombre} seleccionado (stock actual: {repuestoSeleccionado.stock_actual})
            </span>
          )}
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

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            style={styles.btnLimpiar}
            type="button"
            onClick={limpiarFormulario}
          >
            Limpiar formulario
          </button>
          <button
            style={{
              ...styles.btn,
              flex: 1,
              ...(loading || !form.repuesto_id ? { opacity: 0.7, cursor: 'not-allowed' } : {}),
            }}
            type="submit"
            disabled={loading || !form.repuesto_id}
          >
            {loading ? 'Registrando...' : `Registrar ${tipo}`}
          </button>
        </div>
      </form>
    </div>
  );
}

const styles = {
  page: { padding: '1.5rem', fontFamily: 'system-ui, sans-serif', maxWidth: '600px' },
  titulo: { color: '#1B3A5C', marginBottom: '1.25rem' },
  tabs: { display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' },
  tab: {
    padding: '0.55rem 1rem', border: '2px solid #1B3A5C',
    borderRadius: '6px', background: '#fff', cursor: 'pointer', fontWeight: '500',
  },
  tabActivo: { background: '#1B3A5C', color: '#fff' },
  form: {
    background: '#fff', border: '1px solid #e2e8f0',
    borderRadius: '10px', padding: '1.5rem',
    display: 'flex', flexDirection: 'column', gap: '1rem',
  },
  field: { display: 'flex', flexDirection: 'column', gap: '0.3rem' },
  label: { fontSize: '0.85rem', fontWeight: '600', color: '#374151' },
  input: { padding: '0.55rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  autocompleteWrapper: { position: 'relative' },
  lista: {
    position: 'absolute', top: '100%', left: 0, right: 0, zIndex: 100,
    background: '#fff', border: '1px solid #d1d5db', borderRadius: '6px',
    boxShadow: '0 4px 16px rgba(0,0,0,0.12)', margin: '2px 0 0 0',
    padding: 0, listStyle: 'none', maxHeight: '240px', overflowY: 'auto',
  },
  listaItem: {
    padding: '0.6rem 0.85rem', cursor: 'pointer', background: '#fff',
    display: 'flex', flexDirection: 'column', gap: '0.1rem',
    borderBottom: '1px solid #f3f4f6',
  },
  listaItemNombre: { fontSize: '0.9rem', fontWeight: '600', color: '#1B3A5C' },
  listaItemMeta: { fontSize: '0.78rem', color: '#6b7280' },
  repuestoConfirmado: {
    fontSize: '0.8rem', color: '#16a34a', fontWeight: '600', marginTop: '0.2rem',
  },
  btn: {
    background: '#1B3A5C', color: '#fff', border: 'none',
    borderRadius: '6px', padding: '0.7rem', fontSize: '1rem',
    cursor: 'pointer', fontWeight: '600',
  },
  btnLimpiar: {
    background: '#f3f4f6', color: '#374151', border: '1px solid #d1d5db',
    borderRadius: '6px', padding: '0.7rem 1rem', fontSize: '0.9rem',
    cursor: 'pointer', fontWeight: '500',
  },
  ok: { color: '#16a34a', fontWeight: '600', margin: 0 },
  error: { color: '#dc2626', margin: 0 },
};
