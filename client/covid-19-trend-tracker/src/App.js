import './App.css';
import { BrowserRouter as Router } from 'react-router-dom';
import { ToastProvider } from './hooks/use-toast';
import PageLayout from './components/layout/pagelayout';

function App() {
  return (
    <Router>
      <ToastProvider>
        <PageLayout>

        </PageLayout>
      </ToastProvider>
    </Router>
  );
}

export default App;
