// App.jsx
// Responsabilidad: routing principal y manejo de sesión.
// Trazabilidad: REQ-NF02

import { useState } from 'react';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Repuestos from './pages/Repuestos';
import Movimientos from './pages/Movimientos';

const NAV = [
  { key: 'dashboard', label: '🏠 Dashboard' },
  { key: 'repuestos', label: '🔩 Repuestos' },
  { key: 'movimientos', label: '📦 Movimientos' },
];

export default function App() {
  const [session, setSession] = useState(null);
  const [pagina, setPagina] = useState('dashboard');

  if (!session) {
    return <Login onLogin={setSession} />;
  }

  const renderPagina = () => {
    if (pagina === 'repuestos') return <Repuestos />;
    if (pagina === 'movimientos') return <Movimientos />;
    return <Dashboard onLogout={() => setSession(null)} />;
  };

  return (
    <div style={styles.layout}>
      <nav style={styles.nav}>
        <div style={styles.navTitle}>AutoBhan</div>
        {NAV.map((n) => (
          <button
            key={n.key}
            style={{ ...styles.navBtn, ...(pagina === n.key ? styles.navBtnActivo : {}) }}
            onClick={() => setPagina(n.key)}
          >
            {n.label}
          </button>
        ))}
        <button style={styles.navBtnLogout} onClick={() => setSession(null)}>
          Cerrar sesión
        </button>
      </nav>
      <main style={styles.main}>{renderPagina()}</main>
    </div>
  );
}

const styles = {
  layout: { display: 'flex', minHeight: '100vh', fontFamily: 'system-ui, sans-serif' },
  nav: {
    width: '210px', background: '#1B3A5C', display: 'flex',
    flexDirection: 'column', padding: '1rem 0', flexShrink: 0,
  },
  navTitle: { color: '#fff', fontWeight: 'bold', fontSize: '1.1rem', padding: '0.5rem 1rem 1.5rem' },
  navBtn: {
    background: 'transparent', color: '#cbd5e1', border: 'none',
    textAlign: 'left', padding: '0.7rem 1rem', cursor: 'pointer',
    fontSize: '0.9rem', borderLeft: '3px solid transparent',
  },
  navBtnActivo: { color: '#fff', background: 'rgba(255,255,255,0.1)', borderLeftColor: '#38bdf8' },
  navBtnLogout: {
    marginTop: 'auto', background: 'transparent', color: '#94a3b8',
    border: 'none', textAlign: 'left', padding: '0.7rem 1rem', cursor: 'pointer', fontSize: '0.85rem',
  },
  main: { flex: 1, background: '#f0f4f8', overflow: 'auto' },
};
