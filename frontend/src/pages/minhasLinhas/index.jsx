import { useState, useEffect } from 'react';
import axios from 'axios';
import './style.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

function Linhas() {
  const [linhas, setLinhas] = useState([]);
  const navigate = useNavigate();
  const { usuario } = useAuth();

  useEffect(() => {
    if (!usuario) {
      navigate('/');
      return;
    }

    carregarLinhas();
  }, [usuario, navigate]);

  const carregarLinhas = () => {
    axios.get(`http://localhost:8000/paradas/usuario/${usuario.id}`)
      .then(res => {
        setLinhas(res.data);
      })
      .catch(() => {
        toast.error('Erro ao carregar as linhas.');
      });
  };

  const handleCadastrar = () => {
    navigate('/cadastrar-linha');
  };

  const handleEditarPerfil = () => {
    navigate('/editar-perfil');
  };

  const handleLogout = () => {
    localStorage.removeItem('usuario');
    navigate('/');
  };

  const handleExcluir = (id) => {
    if (!window.confirm('Tem certeza que deseja excluir essa parada?')) return;

    axios.delete(`http://localhost:8000/paradas/${id}`)
      .then(() => {
        toast.success('Parada excluída com sucesso.');
        setLinhas(prev => prev.filter(linha => linha.id !== id));
      })
      .catch(() => {
        toast.error('Erro ao excluir a parada.');
      });
  };

  return (
    <div className="container">
      <div className="logo-area">
        <img src="/autocarro.png" alt="Logo" className="logo" />
        <h1>Lá Vem em 10 - Linhas</h1>
      </div>

      <div className="top-buttons">
        <button className="editar-perfil-button" onClick={handleEditarPerfil}>Editar Perfil</button>
        <button className="logout-button" onClick={handleLogout}>Sair</button>
      </div>

      <div className="linha-lista">
        <h2>Linhas Cadastradas</h2>
        {linhas.length > 0 ? (
          <ul>
            {linhas.map(linha => (
              <li key={linha.id} className="linha-item">
                <div className="linha-info">
                  {linha.linha} - {linha.ponto} - {linha.janela_horario_inicio} até {linha.janela_horario_fim}
                </div>
                <div className="linha-botoes">
                  <button className="ver-mapa-button" onClick={() => navigate(`/parada/${linha.id}/mapa`, { state: { latitude: linha.latitude, longitude: linha.longitude, ponto: linha.ponto, linha: linha.linha } })}>
                    Ver no mapa
                  </button>
                  <button className="excluir-button" onClick={() => handleExcluir(linha.id)}>Excluir</button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>Nenhuma linha cadastrada.</p>
        )}
      </div>

      <button className="cadastro-button" onClick={handleCadastrar}>Cadastrar Nova Linha</button>

      <ToastContainer />
    </div>
  );
}

export default Linhas;
