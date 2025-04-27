import { useState } from 'react';
import axios from 'axios';
import './style.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom'; // Importando o useNavigate

function Cadastro() {
  const [login, setLogin] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const navigate = useNavigate(); // Hook para navegação

  const handleSubmit = (e) => {
    e.preventDefault(); // Previne o envio padrão do formulário

    const userData = {
      login: login,
      email: email,
      senha: senha,
    };

    // Realiza a requisição POST para o backend
    axios.post('http://localhost:8000/usuarios/criar', userData)
      .then((response) => {
        // Limpa os campos diretamente com os setters
        setLogin('');
        setEmail('');
        setSenha('');

        // Mostra mensagem de sucesso
        toast.success('Usuário cadastrado com sucesso!');
      })
      .catch((error) => {
        const erroDetalhe = error.response?.data?.detail;

        if (erroDetalhe === "Login já está em uso.") {
          toast.warning('Esse login já está em uso. Tente outro.');
        } else if (erroDetalhe === "Email já está em uso.") {
          toast.warning("Esse e-mail já está cadastrado. Use outro.");
        } else {
          toast.error("Erro ao cadastrar usuário.");
        }
      });
  }

  // Função para navegar para a tela de Login
  const handleGoToLogin = () => {
    navigate('/');
  }

  return (
    <div className='container'>
      
      <div className="logo-area">
        <img src="/autocarro.png" alt="Logo" className="logo" />
        <h1>Lá Vem em 10</h1>
      </div>


      <form onSubmit={handleSubmit}>
        <h3>Login</h3>
        <input
          name='login'
          type="text"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
        />
        <h3>Email</h3>
        <input
          name='email'
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <h3>Senha</h3>
        <input
          name='senha'
          type="password"
          value={senha}
          onChange={(e) => setSenha(e.target.value)}
          required
        />
        <button type='submit'>Cadastrar</button>
      </form>

      <div className='titulo-container'>
          <button type="button" onClick={handleGoToLogin} className="back-to-login-button">
            Voltar
          </button>
          <h2 className="titulo-texto">Faça o seu cadastro</h2>
      </div>


      <ToastContainer />
    </div>
  );
}

export default Cadastro;
