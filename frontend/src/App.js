import logo from './logo.svg';
import './App.css';
import { Routes, Route } from 'react-router-dom';
import ChatUI from './Components/ChatUI';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/test" element={<ChatUI />} />
      </Routes>
    </div>
  );
}

export default App;
