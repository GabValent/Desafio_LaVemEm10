import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './style.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Icon } from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';

function CadastroParada() {
  const [linha, setLinha] = useState('');
  const [ponto, setPonto] = useState(''); // Armazenar o nome do ponto
  const [janelaInicio, setJanelaInicio] = useState('');
  const [janelaFim, setJanelaFim] = useState('');
  const [linhasDisponiveis, setLinhasDisponiveis] = useState([]);
  const [pontosDisponiveis, setPontosDisponiveis] = useState([]);
  const [selectedPonto, setSelectedPonto] = useState(null); // Para armazenar a latitude e longitude do ponto selecionado
  const { usuario } = useAuth();
  const navigate = useNavigate();

  const customIcon = new Icon({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIcon2x,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });

  // Coordenadas iniciais do mapa (caso não haja ponto selecionado)
  const initialCoords = [51.505, -0.09]; // Exemplo de coordenadas iniciais (Londres, por exemplo)

  const mapRef = useRef();

  // Carregar as linhas disponíveis ao montar o componente
  useEffect(() => {
    axios.get('http://localhost:8000/onibus/linhas')
      .then(response => {
        setLinhasDisponiveis(response.data);
      })
      .catch(error => {
        toast.error('Erro ao carregar linhas.');
      });
  }, []);

  // Quando a linha é selecionada, buscar os pontos dessa linha
  useEffect(() => {
    if (linha) {
      toast.info('Buscando pontos da linha...');
      axios.get('http://localhost:8000/onibus/busca', { params: { numero_linha: linha } })
        .then(response => {
          setPontosDisponiveis(response.data);
          toast.dismiss();  // Fechar o toast de "buscando" se a requisição for bem-sucedida
        })
        .catch(error => {
          toast.error('Erro ao carregar pontos.');
        });
    }
  }, [linha]);

  // Função para cadastrar uma nova parada
  const handleCadastro = (e) => {
    e.preventDefault();

    if (!selectedPonto) {
      toast.error('Ponto inválido ou não encontrado.');
      return;
    }

    const novaParada = {
      usuario_id: usuario.id,
      linha,
      ponto,
      janela_horario_inicio: janelaInicio,
      janela_horario_fim: janelaFim,
      latitude: selectedPonto.lat,
      longitude: selectedPonto.lon,
    };

    axios.post('http://localhost:8000/paradas/criar', novaParada)
      .then(res => {
        toast.success('Parada cadastrada com sucesso!');
        navigate('/linhas'); // Redireciona para a tela de paradas cadastradas
      })
      .catch(error => {
        toast.error('Erro ao cadastrar a parada.');
      });
  };

  const handlePontoChange = (e) => {
    const pontoSelecionado = pontosDisponiveis.find(p => p.nome === e.target.value);
    setPonto(e.target.value);  // nome
    setSelectedPonto(pontoSelecionado);  // objeto com id, nome, lat, lon, etc
  };

  // Atualizar o mapa quando selectedPonto mudar
  useEffect(() => {
    if (selectedPonto && mapRef.current) {
      const map = mapRef.current;
      map.setView([selectedPonto.lat, selectedPonto.lon], 16);
    }
  }, [selectedPonto]);

  return (
    <div className="container">
      <div className="logo-area">
        <img src="/autocarro.png" alt="Logo" className="logo" />
        <h1>Lá Vem em 10 - Cadastro de Parada</h1>
      </div>

      <div className='form-mapaTelaCadastro'>
      <form onSubmit={handleCadastro}>
        <div className="titulo-container">
          <h2 className="titulo-texto">Cadastro de Parada</h2>
        </div>
        <label htmlFor="linha">Linha</label>
        <select
          id="linha"
          value={linha}
          onChange={(e) => setLinha(e.target.value)}
          required
        >
          <option value="">-- Escolha uma linha --</option>
          {linhasDisponiveis.map((linha) => (
            <option key={linha.id} value={linha.numero_linha}>
              {linha.numero_linha} - {linha.nome_linha}
            </option>
          ))}
        </select>

        <label htmlFor="ponto">Ponto</label>
        <select
          id="ponto"
          value={ponto}
          onChange={handlePontoChange}  // Alterado para handlePontoChange
          required
        >
          <option value="">-- Escolha um ponto --</option>
          {pontosDisponiveis.map((ponto) => (
            <option key={ponto.id} value={ponto.nome}>
              {ponto.nome}
            </option>
          ))}
        </select>

        <label htmlFor="janelaInicio">Janela Início</label>
        <input
          type="time"
          id="janelaInicio"
          value={janelaInicio}
          onChange={(e) => setJanelaInicio(e.target.value)}
          required
        />

        <label htmlFor="janelaFim">Janela Fim</label>
        <input
          type="time"
          id="janelaFim"
          value={janelaFim}
          onChange={(e) => setJanelaFim(e.target.value)}
          required
        />

        <button type="submit">Cadastrar</button>
      </form>

      <MapContainer
        ref={mapRef}
        center={selectedPonto ? [selectedPonto.lat, selectedPonto.lon] : initialCoords}
        zoom={16}
        style={{ width: '100%', height: '400px' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {selectedPonto && (
          <Marker position={[selectedPonto.lat, selectedPonto.lon]} icon={customIcon}>
            <Popup>Parada: {ponto}</Popup>
          </Marker>
        )}
      </MapContainer>

      </div>

      <button className="voltar-button" onClick={() => navigate('/linhas')}>
        Voltar
      </button>
      <ToastContainer />
    </div>
  );
}

export default CadastroParada;
