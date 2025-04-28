import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useAuth } from '../../context/AuthContext';

function EditarPerfil() {
  const [usuario, setUsuario] = useState({
    login: '',
    email: '',
    senha: ''
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { usuario: usuarioContext } = useAuth();

  useEffect(() => {
    if (!usuarioContext) {
      navigate('/');
      return;
    }
    setUsuario({
      login: usuarioContext.login,
      email: usuarioContext.email,
      senha: usuarioContext.senha,
    });
  }, [usuarioContext, navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    const dados = {
      login: usuario.login,
      email: usuario.email,
      senha: usuario.senha,
    };

    axios.put(`http://localhost:8000/usuarios/${usuarioContext.id}`, dados)
      .then((response) => {
        toast.success('Usuário atualizado com sucesso!');
        navigate('/linhas'); // Redireciona após sucesso
      })
      .catch((error) => {
        const erroDetalhe = error.response?.data?.detail;
        if (erroDetalhe === "Login já está em uso.") {
          toast.warning('Esse login já está em uso. Tente outro.');
        } else if (erroDetalhe === "Email já está em uso.") {
          toast.warning("Esse e-mail já está cadastrado. Use outro.");
        } else {
          toast.error("Erro ao atualizar usuário.");
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="container">
      <div className="logo-area">
        <img src="/autocarro.png" alt="Logo" className="logo" />
        <h1>Editar Perfil</h1>
      </div>

      <form onSubmit={handleSubmit} className="form">
        <label> Login: </label>
          <input
            type="text"
            value={usuario.login}
            onChange={(e) => setUsuario({ ...usuario, login: e.target.value })}
          />
 

        <label> E-mail: </label>
          <input
            type="email"
            value={usuario.email}
            onChange={(e) => setUsuario({ ...usuario, email: e.target.value })}
          />

        <label> Senha: </label>
          <input
            type="password"
            value={usuario.senha}
            onChange={(e) => setUsuario({ ...usuario, senha: e.target.value })}
          />


        <button type="submit" disabled={loading}>
          {loading ? 'Atualizando...' : 'Atualizar'}
        </button>
      </form>

      <button className="voltar-button" onClick={() => navigate('/linhas')}>
        Voltar
      </button>

      <ToastContainer />
    </div>
  );
}

export default EditarPerfil;
