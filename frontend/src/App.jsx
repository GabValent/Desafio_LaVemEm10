import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/login';
import Cadastro from './pages/cadastro';
import PrivateRoute from './components/PrivateRoute';
import { AuthProvider } from './context/AuthContext';
import Linhas from './pages/minhasLinhas';
import CadastroLinha from './pages/cadastrarLinhas';
import ParadaMapa from './pages/mapa';
import EditarPerfil from './pages/editarPerfil';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          
          <Route path="/parada/:id/mapa" element={
            <PrivateRoute>
              <ParadaMapa />
            </PrivateRoute>
          } />

          <Route path="/linhas" element={
            <PrivateRoute>
              <Linhas />
            </PrivateRoute>
          } />

          <Route path="/cadastrar-linha" element={
            <PrivateRoute>
              <CadastroLinha />
            </PrivateRoute>
          } />
          <Route path="/editar-perfil" element={
            <PrivateRoute>
              <EditarPerfil />
            </PrivateRoute>
          } />
          
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
