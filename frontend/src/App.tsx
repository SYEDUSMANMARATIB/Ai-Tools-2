import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';

// Components
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import DocumentUpload from './pages/DocumentUpload';
import ProcessingStatus from './pages/ProcessingStatus';
import Results from './pages/Results';
import AuditDashboard from './pages/AuditDashboard';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />

          <Header />

          <div className="flex">
            <Sidebar />

            <main className="flex-1 p-6 ml-64">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <Routes>
                  <Route path="/" element={<DocumentUpload />} />
                  <Route path="/upload" element={<DocumentUpload />} />
                  <Route path="/processing" element={<ProcessingStatus />} />
                  <Route path="/results" element={<Results />} />
                  <Route path="/audit" element={<AuditDashboard />} />
                </Routes>
              </motion.div>
            </main>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
