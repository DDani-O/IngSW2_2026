// pages/Historial.jsx
// Responsabilidad: historial completo de movimientos con datos del repuesto.
// Permite filtrar por tipo, repuesto y empleado.
// Trazabilidad: REQ-F02, REQ-F03

import { useState, useEffect, useCallback } from 'react';
import { historialService, repuestosService } from '../services/api';

const BADGE = {
  entrada: { bg: '#dcfce7', color: '#166534', label: '▲ Entrada' },
  salida:  { bg: '#fef2f2', color: '#991b1b', label: '▼ Salida' },
};

function formatFecha(fechaStr) {
  const [y, m, d] = fechaStr.split('-');
  return `${d}/${m}/${y}`;
}

function formatHora(isoStr) {
  const d = new Date(isoStr);
  return d.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' });
}

export default function Historial() {
  const [movimientos, setMovimientos] = useState([]);
  const [repuestos, setRepuestos]     = useState([]);
  const [loading, setLoading]         = useState(true);
  const [error, setError]             = useState('');

  const [filtroTipo,      setFiltroTipo]      = useState('');
  const [filtroRepuesto,  setFiltroRepuesto]  = useState('');
  const [filtroEmpleado,  setFiltroEmpleado]  = useState('');
  const [filtroDesde,     setFiltroDesde]     = useState('');
  const [filtroHasta,     setFiltroHasta]     = useState('');

  useEffect(() => {
    repuestosService.listar().then(setRepuestos).catch(() => {});
  }, []);

  const cargar = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = {};
      if (filtroTipo)     params.tipo       = filtroTipo;
      if (filtroRepuesto) params.repuesto_id = filtroRepuesto;
      if (filtroEmpleado) params.empleado   = filtroEmpleado;
      if (filtroDesde)    params.fecha_desde = filtroDesde;
      if (filtroHasta)    params.fecha_hasta = filtroHasta;
      const data = await historialService.listar(params);
      setMovimientos(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [filtroTipo, filtroRepuesto, filtroEmpleado, filtroDesde, filtroHasta]);

  useEffect(() => { cargar(); }, [cargar]);

  const limpiar = () => {
    setFiltroTipo('');
    setFiltroRepuesto('');
    setFiltroEmpleado('');
    setFiltroDesde('');
    setFiltroHasta('');
  };

  const entradas = movimientos.filter(m => m.tipo === 'entrada').reduce((s, m) => s + m.cantidad, 0);
  const salidas  = movimientos.filter(m => m.tipo === 'salida').reduce((s, m) => s + m.cantidad, 0);

  return (
    <div style={s.page}>
      <h2 style={s.titulo}>Historial de Movimientos</h2>

      {/* Filtros */}
      <div style={s.filtrosBox}>
        <select style={s.input} value={filtroTipo} onChange={e => setFiltroTipo(e.target.value)}>
          <option value="">Todos los tipos</option>
          <option value="entrada">▲ Entradas</option>
          <option value="salida">▼ Salidas</option>
        </select>

        <select style={s.input} value={filtroRepuesto} onChange={e => setFiltroRepuesto(e.target.value)}>
          <option value="">Todos los repuestos</option>
          {repuestos.map(r => (
            <option key={r.id} value={r.id}>{r.nombre} — {r.marca}</option>
          ))}
        </select>

        <input
          style={s.input}
          placeholder="Buscar por empleado..."
          value={filtroEmpleado}
          onChange={e => setFiltroEmpleado(e.target.value)}
        />

        <div style={s.fechas}>
          <input
            style={s.inputFecha}
            type="date"
            value={filtroDesde}
            onChange={e => setFiltroDesde(e.target.value)}
            title="Desde"
          />
          <span style={{ color: '#94a3b8', fontSize: '0.85rem' }}>hasta</span>
          <input
            style={s.inputFecha}
            type="date"
            value={filtroHasta}
            onChange={e => setFiltroHasta(e.target.value)}
            title="Hasta"
          />
        </div>

        {(filtroTipo || filtroRepuesto || filtroEmpleado || filtroDesde || filtroHasta) && (
          <button style={s.btnLimpiar} onClick={limpiar}>✕ Limpiar</button>
        )}
      </div>

      {/* Resumen */}
      {!loading && movimientos.length > 0 && (
        <div style={s.resumen}>
          <div style={s.chip}>
            <span style={s.chipNum}>{movimientos.length}</span>
            <span style={s.chipLabel}>movimientos</span>
          </div>
          <div style={{ ...s.chip, borderColor: '#16a34a' }}>
            <span style={{ ...s.chipNum, color: '#16a34a' }}>+{entradas}</span>
            <span style={s.chipLabel}>unidades ingresadas</span>
          </div>
          <div style={{ ...s.chip, borderColor: '#dc2626' }}>
            <span style={{ ...s.chipNum, color: '#dc2626' }}>-{salidas}</span>
            <span style={s.chipLabel}>unidades retiradas</span>
          </div>
        </div>
      )}

      {/* Estado */}
      {loading && <p style={{ color: '#64748b', padding: '1rem 0' }}>Cargando...</p>}
      {error && <p style={{ color: '#dc2626' }}>Error: {error}</p>}
      {!loading && movimientos.length === 0 && (
        <p style={{ color: '#64748b', padding: '1rem 0' }}>No hay movimientos para mostrar.</p>
      )}

      {/* Tabla */}
      {!loading && movimientos.length > 0 && (
        <div style={s.tableWrap}>
          <table style={s.tabla}>
            <thead>
              <tr>
                {['Fecha', 'Tipo', 'Repuesto', 'Categoría', 'Marca', 'N° Serie',
                  'Cantidad', 'Empleado', 'Detalle', 'Stock actual'].map(h => (
                  <th key={h} style={s.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {movimientos.map((m, i) => {
                const badge = BADGE[m.tipo];
                return (
                  <tr key={m.id} style={{ background: i % 2 === 0 ? '#fff' : '#f8fafc' }}>
                    <td style={s.td}>
                      <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>
                        {formatFecha(m.fecha)}
                      </div>
                      <div style={{ color: '#94a3b8', fontSize: '0.75rem' }}>
                        {formatHora(m.created_at)}
                      </div>
                    </td>
                    <td style={s.td}>
                      <span style={{
                        ...s.badge,
                        background: badge.bg,
                        color: badge.color,
                      }}>
                        {badge.label}
                      </span>
                    </td>
                    <td style={{ ...s.td, fontWeight: 600 }}>{m.repuesto_nombre}</td>
                    <td style={s.td}>{m.repuesto_categoria}</td>
                    <td style={s.td}>{m.repuesto_marca}</td>
                    <td style={{ ...s.td, fontFamily: 'monospace', fontSize: '0.8rem', color: '#64748b' }}>
                      {m.repuesto_numero_serie}
                    </td>
                    <td style={{
                      ...s.td,
                      fontWeight: 700,
                      fontSize: '1rem',
                      color: m.tipo === 'entrada' ? '#16a34a' : '#dc2626',
                      textAlign: 'center',
                    }}>
                      {m.tipo === 'entrada' ? '+' : '-'}{m.cantidad}
                    </td>
                    <td style={s.td}>{m.empleado}</td>
                    <td style={{ ...s.td, color: '#475569', fontSize: '0.85rem' }}>
                      {m.tipo === 'entrada'
                        ? `Proveedor: ${m.proveedor || '—'}`
                        : `Finalidad: ${m.finalidad || '—'}`}
                    </td>
                    <td style={{ ...s.td, textAlign: 'center', fontWeight: 600 }}>
                      {m.stock_actual}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const s = {
  page:       { padding: '1.5rem', fontFamily: 'system-ui, sans-serif' },
  titulo:     { color: '#1B3A5C', marginBottom: '1.25rem' },
  filtrosBox: {
    display: 'flex', flexWrap: 'wrap', gap: '0.75rem',
    marginBottom: '1.25rem', alignItems: 'center',
  },
  input: {
    padding: '0.5rem 0.75rem', border: '1px solid #d1d5db',
    borderRadius: '6px', fontSize: '0.9rem', minWidth: '180px',
    background: '#fff',
  },
  inputFecha: {
    padding: '0.5rem 0.6rem', border: '1px solid #d1d5db',
    borderRadius: '6px', fontSize: '0.85rem',
  },
  fechas:     { display: 'flex', alignItems: 'center', gap: '0.5rem' },
  btnLimpiar: {
    padding: '0.5rem 1rem', border: '1px solid #e2e8f0',
    borderRadius: '6px', background: '#f8fafc', cursor: 'pointer',
    fontSize: '0.85rem', color: '#64748b',
  },
  resumen:    { display: 'flex', gap: '1rem', marginBottom: '1.25rem', flexWrap: 'wrap' },
  chip: {
    display: 'flex', flexDirection: 'column', alignItems: 'center',
    background: '#fff', border: '2px solid #e2e8f0', borderRadius: '8px',
    padding: '0.6rem 1.2rem',
  },
  chipNum:    { fontSize: '1.5rem', fontWeight: 700, color: '#1B3A5C' },
  chipLabel:  { fontSize: '0.75rem', color: '#64748b' },
  tableWrap:  { overflowX: 'auto' },
  tabla:      { width: '100%', borderCollapse: 'collapse', minWidth: '900px', background: '#fff' },
  th: {
    background: '#1B3A5C', color: '#fff', padding: '0.65rem 0.85rem',
    textAlign: 'left', fontSize: '0.8rem', whiteSpace: 'nowrap',
  },
  td:         { padding: '0.6rem 0.85rem', borderBottom: '1px solid #e2e8f0', fontSize: '0.875rem' },
  badge: {
    display: 'inline-block', padding: '0.2rem 0.6rem',
    borderRadius: '999px', fontSize: '0.78rem', fontWeight: 600,
  },
};
