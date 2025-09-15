import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  FileText,
  Download,
  Eye,
  EyeOff,
  Shield,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';

interface RedactionResult {
  id: string;
  filename: string;
  originalText: string;
  redactedText: string;
  entitiesFound: number;
  processingTime: string;
  confidence: number;
  status: 'completed' | 'processing' | 'error';
}

const mockResults: RedactionResult[] = [
  {
    id: '1',
    filename: 'contract_2024.pdf',
    originalText: 'Contact John Doe at john.doe@company.com or call (555) 123-4567 for more information about account #12345678.',
    redactedText: 'Contact ████████ at ████████████████████ or call ██████████████ for more information about account #████████.',
    entitiesFound: 4,
    processingTime: '2.3s',
    confidence: 95.2,
    status: 'completed'
  },
  {
    id: '2',
    filename: 'medical_record.docx',
    originalText: 'Patient SSN: 123-45-6789, DOB: 01/15/1985, Insurance: Blue Cross Policy #ABC123456',
    redactedText: 'Patient SSN: ███████████, DOB: ██████████, Insurance: Blue Cross Policy #█████████',
    entitiesFound: 3,
    processingTime: '1.8s',
    confidence: 98.7,
    status: 'completed'
  }
];

const Results: React.FC = () => {
  const [showOriginal, setShowOriginal] = useState<{ [key: string]: boolean }>({});

  const toggleOriginal = (id: string) => {
    setShowOriginal(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Redaction Results
        </h1>
        <p className="text-gray-600">
          Review and download your redacted documents
        </p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
        >
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Documents</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
        >
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Items Redacted</p>
              <p className="text-2xl font-bold text-gray-900">89</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
        >
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-purple-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg. Time</p>
              <p className="text-2xl font-bold text-gray-900">2.1s</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
        >
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">98.5%</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Results List */}
      <div className="space-y-6">
        {mockResults.map((result, index) => (
          <motion.div
            key={result.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
          >
            {/* Header */}
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileText className="h-6 w-6 text-blue-600" />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {result.filename}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span>{result.entitiesFound} entities found</span>
                      <span>Processed in {result.processingTime}</span>
                      <span className="flex items-center">
                        <CheckCircle className="h-4 w-4 text-green-500 mr-1" />
                        {result.confidence}% confidence
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => toggleOriginal(result.id)}
                    className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  >
                    {showOriginal[result.id] ? (
                      <>
                        <EyeOff className="h-4 w-4" />
                        <span>Hide Original</span>
                      </>
                    ) : (
                      <>
                        <Eye className="h-4 w-4" />
                        <span>Show Original</span>
                      </>
                    )}
                  </button>
                  <button className="flex items-center space-x-2 px-3 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
                    <Download className="h-4 w-4" />
                    <span>Download</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Content */}
            <div className="px-6 py-4">
              <div className="space-y-4">
                {showOriginal[result.id] && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                      <AlertTriangle className="h-4 w-4 text-amber-500 mr-2" />
                      Original Text (Sensitive)
                    </h4>
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <p className="text-sm text-gray-800 font-mono">
                        {result.originalText}
                      </p>
                    </div>
                  </div>
                )}

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                    <Shield className="h-4 w-4 text-green-500 mr-2" />
                    Redacted Text (Safe)
                  </h4>
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <p className="text-sm text-gray-800 font-mono">
                      {result.redactedText}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Results;
