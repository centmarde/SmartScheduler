import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/Landing';
import TeacherSchedule from './pages/Table';
import { ThemeProvider } from './theme/theme';
import './index.css'

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/table" element={<TeacherSchedule />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App
