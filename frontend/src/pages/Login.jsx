// pages/Login.jsx
// Responsabilidad: pantalla de inicio de sesión del administrador.
// Llama a POST /auth/login en el backend — nunca habla directo con Supabase.
// Trazabilidad: REQ-NF02

import { useState } from 'react';
import { authService, setToken } from '../services/api';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await authService.login(email, password);
      setToken(data.access_token);
      onLogin({ email: data.user_email, token: data.access_token });
    } catch (err) {
      setError('Credenciales inválidas. Verificá tu email y contraseña.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>🔧 AutoBhan Autopartes</h1>
        <p style={styles.subtitle}>Sistema de Gestión de Inventario</p>
        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>Email</label>
          <input
            style={styles.input}
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="admin@autobhan.com"
          />
          <label style={styles.label}>Contraseña</label>
          <input
            style={styles.input}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.btn} type="submit" disabled={loading}>
            {loading ? 'Ingresando...' : 'Ingresar'}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh', display: 'flex',
    alignItems: 'center', justifyContent: 'center',
    background: '#f0f4f8',
  },
  card: {
    background: '#fff', padding: '2.5rem', borderRadius: '12px',
    boxShadow: '0 4px 20px rgba(0,0,0,0.1)', width: '100%', maxWidth: '380px',
  },
  title: { margin: 0, fontSize: '1.5rem', color: '#1B3A5C', textAlign: 'center' },
  subtitle: { color: '#64748b', textAlign: 'center', marginBottom: '1.5rem', fontSize: '0.9rem' },
  form: { display: 'flex', flexDirection: 'column', gap: '0.75rem' },
  label: { fontSize: '0.875rem', fontWeight: '600', color: '#374151' },
  input: {
    padding: '0.6rem 0.8rem', border: '1px solid #d1d5db',
    borderRadius: '6px', fontSize: '0.95rem', outline: 'none',
  },
  btn: {
    marginTop: '0.5rem', padding: '0.75rem', background: '#1B3A5C',
    color: '#fff', border: 'none', borderRadius: '6px',
    fontSize: '1rem', cursor: 'pointer', fontWeight: '600',
  },
  error: { color: '#dc2626', fontSize: '0.875rem', margin: 0 },
};
