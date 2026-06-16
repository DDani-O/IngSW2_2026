// pages/Repuestos.jsx
// Responsabilidad: listado, filtros, registro, edición y eliminación de repuestos.
// Trazabilidad: REQ-F01, REQ-F04

import { useState, useEffect, useCallback } from 'react';
import { repuestosService } from '../services/api';

const CATEGORIAS = ['', 'auto', 'moto', 'camioneta'];
const FORM_VACIO = { nombre: '', categoria: 'auto', marca: '', numero_serie: '', precio: '', stock_inicial: '', stock_minimo: '5' };
const EDIT_VACIO = { nombre: '', categoria: 'auto', marca: '', numero_serie: '', precio: '', stock_minimo: '' };

export default function Repuestos() {
  const [repuestos, setRepuestos] = useState([]);
  const [filtroCategoria, setFiltroCategoria] = useState('');
  const [filtroNombre, setFiltroNombre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Crear
  const [mostrarForm, setMostrarForm] = useState(false);
  const [form, setForm] = useState(FORM_VACIO);

  // Editar
  const [editandoId, setEditandoId] = useState(null);
  const [formEdit, setFormEdit] = useState(EDIT_VACIO);
  const [errorEdit, setErrorEdit] = useState('');

  // Eliminar
  const [confirmarEliminar, setConfirmarEliminar] = useState(null); // { id, nombre }
  const [eliminando, setEliminando] = useState(false);

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

  // ── Crear ──────────────────────────────────────────────────────────────────
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
      setForm(FORM_VACIO);
      cargarRepuestos();
    } catch (e) {
      setError(e.message);
    }
  };

  // ── Editar ─────────────────────────────────────────────────────────────────
  const abrirEdicion = (r) => {
    setEditandoId(r.id);
    setFormEdit({
      nombre: r.nombre,
      categoria: r.categoria,
      marca: r.marca,
      numero_serie: r.numero_serie,
      precio: String(r.precio),
      stock_minimo: String(r.stock_minimo),
    });
    setErrorEdit('');
  };

  const cancelarEdicion = () => {
    setEditandoId(null);
    setFormEdit(EDIT_VACIO);
    setErrorEdit('');
  };

  const handleEditar = async (e, id) => {
    e.preventDefault();
    setErrorEdit('');
    try {
      await repuestosService.actualizar(id, {
        nombre: formEdit.nombre,
        categoria: formEdit.categoria,
        marca: formEdit.marca,
        numero_serie: formEdit.numero_serie,
        precio: parseFloat(formEdit.precio),
        stock_minimo: parseInt(formEdit.stock_minimo, 10),
      });
      setEditandoId(null);
      cargarRepuestos();
    } catch (e) {
      setErrorEdit(e.message);
    }
  };

  // ── Eliminar ───────────────────────────────────────────────────────────────
  const handleEliminar = async () => {
    if (!confirmarEliminar) return;
    setEliminando(true);
    try {
      await repuestosService.eliminar(confirmarEliminar.id);
      setConfirmarEliminar(null);
      cargarRepuestos();
    } catch (e) {
      setError(e.message);
      setConfirmarEliminar(null);
    } finally {
      setEliminando(false);
    }
  };

  return (
    <div style={styles.page}>

      {/* ── Popup de confirmación de eliminación ── */}
      {confirmarEliminar && (
        <div style={styles.overlay}>
          <div style={styles.popup}>
            <h3 style={styles.popupTitulo}>⚠️ Confirmar eliminación</h3>
            <p style={styles.popupTexto}>
              ¿Estás seguro de que querés eliminar <strong>{confirmarEliminar.nombre}</strong>?
              Esta acción no se puede deshacer.
            </p>
            <div style={styles.popupBtns}>
              <button
                style={styles.btnCancelar}
                onClick={() => setConfirmarEliminar(null)}
                disabled={eliminando}
              >
                Cancelar
              </button>
              <button
                style={styles.btnEliminar}
                onClick={handleEliminar}
                disabled={eliminando}
              >
                {eliminando ? 'Eliminando...' : 'Sí, eliminar'}
              </button>
            </div>
          </div>
        </div>
      )}

      <div style={styles.topBar}>
        <h2 style={styles.titulo}>Repuestos</h2>
        <button style={styles.btnPrimary} onClick={() => { setMostrarForm(!mostrarForm); setEditandoId(null); }}>
          {mostrarForm ? 'Cancelar' : '+ Nuevo repuesto'}
        </button>
      </div>

      {/* ── Formulario de creación ── */}
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
              <select style={styles.input} value={form.categoria} onChange={(e) => setForm({ ...form, categoria: e.target.value })}>
                {CATEGORIAS.filter(Boolean).map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btnPrimary} type="submit">Guardar</button>
        </form>
      )}

      {/* ── Filtros ── */}
      <div style={styles.filtros}>
        <select style={styles.select} value={filtroCategoria} onChange={(e) => setFiltroCategoria(e.target.value)}>
          {CATEGORIAS.map((c) => <option key={c} value={c}>{c || 'Todas las categorías'}</option>)}
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

      {/* ── Tabla ── */}
      {!loading && repuestos.length > 0 && (
        <table style={styles.tabla}>
          <thead>
            <tr>
              {['Nombre', 'Categoría', 'Marca', 'N° Serie', 'Precio', 'Stock', 'Mín.', 'Acciones'].map((h) => (
                <th key={h} style={styles.th}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {repuestos.map((r) => (
              editandoId === r.id ? (
                // ── Fila de edición inline ──
                <tr key={r.id} style={{ background: '#EFF6FF' }}>
                  <td style={styles.td}>
                    <input style={styles.inputInline} value={formEdit.nombre} onChange={(e) => setFormEdit({ ...formEdit, nombre: e.target.value })} required />
                  </td>
                  <td style={styles.td}>
                    <select style={styles.inputInline} value={formEdit.categoria} onChange={(e) => setFormEdit({ ...formEdit, categoria: e.target.value })}>
                      {CATEGORIAS.filter(Boolean).map((c) => <option key={c} value={c}>{c}</option>)}
                    </select>
                  </td>
                  <td style={styles.td}>
                    <input style={styles.inputInline} value={formEdit.marca} onChange={(e) => setFormEdit({ ...formEdit, marca: e.target.value })} required />
                  </td>
                  <td style={styles.td}>
                    <input style={styles.inputInline} value={formEdit.numero_serie} onChange={(e) => setFormEdit({ ...formEdit, numero_serie: e.target.value })} required />
                  </td>
                  <td style={styles.td}>
                    <input style={styles.inputInline} type="number" min="0.01" step="0.01" value={formEdit.precio} onChange={(e) => setFormEdit({ ...formEdit, precio: e.target.value })} required />
                  </td>
                  <td style={styles.td}>{r.stock_actual}</td>
                  <td style={styles.td}>
                    <input style={styles.inputInline} type="number" min="0" value={formEdit.stock_minimo} onChange={(e) => setFormEdit({ ...formEdit, stock_minimo: e.target.value })} required />
                  </td>
                  <td style={styles.td}>
                    <div style={styles.accionesFila}>
                      {errorEdit && <span style={{ color: '#dc2626', fontSize: '0.75rem', display: 'block', marginBottom: '0.3rem' }}>{errorEdit}</span>}
                      <button style={styles.btnGuardar} onClick={(e) => handleEditar(e, r.id)}>✓ Guardar</button>
                      <button style={styles.btnCancelarFila} onClick={cancelarEdicion}>✕</button>
                    </div>
                  </td>
                </tr>
              ) : (
                // ── Fila normal ──
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
                  <td style={styles.td}>
                    <div style={styles.accionesFila}>
                      <button style={styles.btnEditar} onClick={() => abrirEdicion(r)}>✏️ Editar</button>
                      <button style={styles.btnEliminarFila} onClick={() => setConfirmarEliminar({ id: r.id, nombre: r.nombre })}>🗑️ Eliminar</button>
                    </div>
                  </td>
                </tr>
              )
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
  form: { background: '#fff', border: '1px solid #e2e8f0', borderRadius: '10px', padding: '1.5rem', marginBottom: '1.5rem' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1rem' },
  field: { display: 'flex', flexDirection: 'column', gap: '0.3rem' },
  label: { fontSize: '0.8rem', fontWeight: '600', color: '#374151' },
  input: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  inputInline: { padding: '0.3rem 0.45rem', border: '1px solid #93c5fd', borderRadius: '4px', fontSize: '0.85rem', width: '100%', boxSizing: 'border-box' },
  filtros: { display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' },
  select: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem' },
  inputFiltro: { padding: '0.5rem', border: '1px solid #d1d5db', borderRadius: '6px', fontSize: '0.9rem', minWidth: '220px' },
  btnPrimary: { background: '#1B3A5C', color: '#fff', border: 'none', borderRadius: '6px', padding: '0.55rem 1.1rem', cursor: 'pointer', fontWeight: '600' },
  tabla: { width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: '8px', overflow: 'hidden' },
  th: { background: '#1B3A5C', color: '#fff', padding: '0.65rem 0.85rem', textAlign: 'left', fontSize: '0.875rem' },
  td: { padding: '0.6rem 0.85rem', borderBottom: '1px solid #e2e8f0', fontSize: '0.9rem', verticalAlign: 'middle' },
  accionesFila: { display: 'flex', gap: '0.4rem', flexWrap: 'wrap' },
  btnEditar: { background: '#EFF6FF', color: '#1d4ed8', border: '1px solid #bfdbfe', borderRadius: '5px', padding: '0.3rem 0.65rem', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600' },
  btnEliminarFila: { background: '#FEF2F2', color: '#dc2626', border: '1px solid #fecaca', borderRadius: '5px', padding: '0.3rem 0.65rem', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600' },
  btnGuardar: { background: '#dcfce7', color: '#166534', border: '1px solid #bbf7d0', borderRadius: '5px', padding: '0.3rem 0.65rem', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600' },
  btnCancelarFila: { background: '#f3f4f6', color: '#374151', border: '1px solid #d1d5db', borderRadius: '5px', padding: '0.3rem 0.55rem', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '600' },
  error: { color: '#dc2626', fontSize: '0.875rem' },
  // Popup
  overlay: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.45)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center' },
  popup: { background: '#fff', borderRadius: '12px', padding: '2rem', maxWidth: '420px', width: '90%', boxShadow: '0 20px 60px rgba(0,0,0,0.25)' },
  popupTitulo: { margin: '0 0 0.75rem', color: '#1B3A5C', fontSize: '1.15rem' },
  popupTexto: { color: '#374151', marginBottom: '1.5rem', lineHeight: '1.5' },
  popupBtns: { display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' },
  btnCancelar: { background: '#f3f4f6', color: '#374151', border: '1px solid #d1d5db', borderRadius: '6px', padding: '0.55rem 1.1rem', cursor: 'pointer', fontWeight: '600' },
  btnEliminar: { background: '#dc2626', color: '#fff', border: 'none', borderRadius: '6px', padding: '0.55rem 1.1rem', cursor: 'pointer', fontWeight: '600' },
};
