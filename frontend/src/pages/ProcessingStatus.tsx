import React from 'react';
import { motion } from 'framer-motion';
import { Clock, CheckCircle, AlertCircle, Loader } from 'lucide-react';

const ProcessingStatus: React.FC = () => {
  const mockJobs = [
    { id: '1', filename: 'contract.pdf', status: 'completed', progress: 100 },
    { id: '2', filename: 'medical.docx', status: 'processing', progress: 65 },
    { id: '3', filename: 'financial.txt', status: 'queued', progress: 0 },
  ];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Processing Status
        </h1>
        <p className="text-gray-600">
          Monitor your document redaction progress
        </p>
      </div>

      <div className="space-y-4">
        {mockJobs.map((job) => (
          <motion.div
            key={job.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                {job.status === 'completed' && <CheckCircle className="h-6 w-6 text-green-500" />}
                {job.status === 'processing' && <Loader className="h-6 w-6 text-blue-500 animate-spin" />}
                {job.status === 'queued' && <Clock className="h-6 w-6 text-gray-400" />}
                <div>
                  <h3 className="font-semibold text-gray-900">{job.filename}</h3>
                  <p className="text-sm text-gray-500 capitalize">{job.status}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{job.progress}%</p>
                <div className="w-32 bg-gray-200 rounded-full h-2 mt-1">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${job.progress}%` }}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ProcessingStatus;
