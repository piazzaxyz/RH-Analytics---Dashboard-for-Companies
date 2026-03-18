import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, Mail, Lock, Loader2, Eye, EyeOff } from 'lucide-react';
import { login, setToken, getToken } from '../services/auth';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (getToken()) navigate('/');
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await login(username, password);
      setToken(data.access_token);
      navigate('/');
    } catch {
      setError('Usuário ou senha inválidos');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo">
            <LayoutDashboard size={40} />
          </div>
          <h1>RH Analytics</h1>
          <p>Entre com suas credenciais para acessar o dashboard</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="login-error">
              {error}
            </div>
          )}
          <div className="login-field">
            <Mail size={20} className="login-field__icon" />
            <input
              type="text"
              placeholder="E-mail ou usuário"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </div>
          <div className="login-field">
            <Lock size={20} className="login-field__icon" />
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
            <button
              type="button"
              className="login-password-toggle"
              onClick={() => setShowPassword(!showPassword)}
              tabIndex={-1}
              aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
          <button type="submit" className="login-submit" disabled={loading}>
            {loading ? <Loader2 size={20} className="spin" /> : 'Entrar'}
          </button>
        </form>

        <p className="login-hint">Use admin@rh.com / admin123 para teste</p>
      </div>
    </div>
  );
};

export default LoginPage;
