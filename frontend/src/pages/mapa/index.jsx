import { useLocation, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import './style.css';
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import { useState, useEffect } from 'react';
import axios from 'axios';

function ParadaMapa() {
  const location = useLocation();
  const navigate = useNavigate();
  const { latitude, longitude, ponto, linha, id } = location.state || {};

  const customIcon = new Icon({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIcon2x,
    shadowUrl: markerShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
  });

  const busIcon = new Icon({
    iconUrl: '/onibus.png',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  const [dadosOnibus, setDadosOnibus] = useState([]);

  useEffect(() => {
    const fetchDadosOnibus = async () => {
      try {
        const res = await axios.get(`http://localhost:8000/onibus/dados_onibus/${linha}`);
        setDadosOnibus(res.data);
      } catch (err) {
        console.error("Erro ao buscar dados do ônibus:", err);
      }
    };

    fetchDadosOnibus();
    const interval = setInterval(fetchDadosOnibus, 30000);
    return () => clearInterval(interval);
  }, [id, linha]);

  if (!latitude || !longitude) {
    return <div className="container-telaMapa"><p>Dados da parada não encontrados.</p></div>;
  }

  return (
    <div className="container-telaMapa">
      <div className="logo-area-telaMapa">
        <img src="/autocarro.png" alt="Logo" className="logo-telaMapa" />
        <h1>Mapa da Parada</h1>
      </div>

      <div className='mapa-tabela'>
        <div className="map-container-telaMapa">
          <MapContainer center={[latitude, longitude]} zoom={16}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            <Marker position={[latitude, longitude]} icon={customIcon}>
              <Popup>Parada: {ponto}</Popup>
            </Marker>

            {dadosOnibus.map((onibus, idx) => (
              <Marker
                key={idx}
                position={[onibus.latitude, onibus.longitude]}
                icon={busIcon}
              >
                <Popup>
                  <strong>Ordem:</strong> {onibus.ordem}<br />
                  <strong>Velocidade:</strong> {onibus.velocidade} km/h<br />
                  <strong>Tempo até a parada:</strong> {Math.round(onibus.tempo_chegada / 60)} min<br />
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        <div className="tabela-container-telaMapa">
          <h2>Ônibus Próximos</h2>
          <table>
            <thead>
              <tr>
                <th>Ordem</th>
                <th>Velocidade (km/h)</th>
                <th>Tempo até parada (min)</th>
              </tr>
            </thead>
            <tbody>
              {dadosOnibus.map((onibus, idx) => (
                <tr key={idx}>
                  <td>{onibus.ordem}</td>
                  <td>{onibus.velocidade}</td>
                  <td>{Math.round(onibus.tempo_chegada / 60)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <button className="voltar-telaMapa" onClick={() => navigate('/linhas')}>
        Voltar
      </button>
    </div>
  );
}

export default ParadaMapa;
