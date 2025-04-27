import { useState } from 'react';
import axios from 'axios';
import './style.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext'

function Login() {
  const [login, setLogin] = useState('');
  const [senha, setSenha] = useState('');
  const navigate = useNavigate();  
  const { login: loginContext } = useAuth();

  const handleLogin = (e) => {
    e.preventDefault();
  
    axios.post('http://localhost:8000/usuarios/login', { login, senha })
      .then(res => {
        const usuario = res.data;
  
        loginContext(usuario);
        navigate('/linhas');
  
      })
      .catch(error => {
        toast.error("Login ou senha inválidos.");
      });
  };

  return (
    <div className="container">
      <div className="logo-area">
        <img src="/autocarro.png" alt="Logo" className="logo" />
        <h1>Lá Vem em 10</h1>
      </div>

      <form onSubmit={handleLogin}>
        <h2>Entrar</h2>

        <label htmlFor="login">Login</label>
        <input
          name="login"
          type="text"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />

        <label htmlFor="senha">Senha</label>
        <input
          name="senha"
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required
        />

        <button type="submit">Entrar</button>
      </form>

      {/* Botão para redirecionar ao cadastro */}
      <button className="link-button" onClick={() => navigate('/cadastro')}>
        Não tem cadastro? Clique aqui
      </button>

      <ToastContainer />
    </div>
  );
}

export default Login;
