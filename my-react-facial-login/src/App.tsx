import FormularioHuella from './FormularioHuella'
import { Login } from './Login'

function App() {
  return (
    <div style={{ padding: 40 }}>
      <h3>Ejercicio de Reconocimiento Facial</h3>
      <Login />
      <FormularioHuella />;
    </div>
  )
}

export default App

