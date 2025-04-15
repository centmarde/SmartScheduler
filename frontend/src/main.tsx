import { createRoot } from 'react-dom/client';
import App from './App.tsx';
// import '@mdi/font/css/materialdesignicons.min.css';

// React Router is configured in App.tsx

// Override console.warn to filter out specific deprecation warnings
const originalWarn = console.warn;
console.warn = (...args) => {
  if (typeof args[0] === 'string' && args[0].includes('ProSidebarProvider is deprecated')) {
    return;
  }
  originalWarn(...args);
};

createRoot(document.getElementById('root')!).render(
  <App />
);