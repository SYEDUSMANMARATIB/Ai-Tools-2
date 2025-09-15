import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

interface UploadedFile {
  file: File;
  id: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
}

const DocumentUpload: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'pending' as const,
      progress: 0,
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);

    // Simulate upload process
    newFiles.forEach(uploadedFile => {
      simulateUpload(uploadedFile.id);
    });
  }, []);

  const simulateUpload = (fileId: string) => {
    setUploadedFiles(prev =>
      prev.map(file =>
        file.id === fileId ? { ...file, status: 'uploading' } : file
      )
    );

    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30;

      setUploadedFiles(prev =>
        prev.map(file =>
          file.id === fileId ? { ...file, progress: Math.min(progress, 100) } : file
        )
      );

      if (progress >= 100) {
        clearInterval(interval);
        setUploadedFiles(prev =>
          prev.map(file =>
            file.id === fileId ? { ...file, status: 'success', progress: 100 } : file
          )
        );
        toast.success('File uploaded successfully!');
      }
    }, 200);
  };

  const removeFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
  });

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Document Redaction Tool
        </h1>
        <p className="text-gray-600">
          Upload your documents to automatically detect and redact sensitive information
        </p>
      </div>

      {/* Upload Area */}
      <motion.div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
          transition-all duration-300 ease-in-out
          ${isDragActive
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
          }
        `}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <input {...getInputProps()} />

        <motion.div
          initial={{ scale: 1 }}
          animate={{ scale: isDragActive ? 1.1 : 1 }}
          transition={{ duration: 0.2 }}
        >
          <Upload className="mx-auto h-16 w-16 text-gray-400 mb-4" />
        </motion.div>

        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          {isDragActive ? 'Drop files here' : 'Upload Documents'}
        </h3>

        <p className="text-gray-600 mb-4">
          Drag and drop your files here, or click to browse
        </p>

        <div className="flex justify-center space-x-4 text-sm text-gray-500">
          <span className="bg-gray-100 px-3 py-1 rounded-full">PDF</span>
          <span className="bg-gray-100 px-3 py-1 rounded-full">DOCX</span>
          <span className="bg-gray-100 px-3 py-1 rounded-full">TXT</span>
        </div>

        <p className="text-xs text-gray-400 mt-4">
          Maximum file size: 50MB
        </p>
      </motion.div>

      {/* Uploaded Files */}
      <AnimatePresence>
        {uploadedFiles.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="mt-8"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Uploaded Files ({uploadedFiles.length})
            </h3>

            <div className="space-y-3">
              {uploadedFiles.map((uploadedFile) => (
                <motion.div
                  key={uploadedFile.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <File className="h-8 w-8 text-blue-500" />
                      <div>
                        <p className="font-medium text-gray-900">
                          {uploadedFile.file.name}
                        </p>
                        <p className="text-sm text-gray-500">
                          {(uploadedFile.file.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      {uploadedFile.status === 'success' && (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      )}
                      {uploadedFile.status === 'error' && (
                        <AlertCircle className="h-5 w-5 text-red-500" />
                      )}

                      <button
                        onClick={() => removeFile(uploadedFile.id)}
                        className="text-gray-400 hover:text-red-500 transition-colors"
                      >
                        <X className="h-5 w-5" />
                      </button>
                    </div>
                  </div>

                  {uploadedFile.status === 'uploading' && (
                    <div className="mt-3">
                      <div className="bg-gray-200 rounded-full h-2">
                        <motion.div
                          className="bg-blue-500 h-2 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${uploadedFile.progress}%` }}
                          transition={{ duration: 0.3 }}
                        />
                      </div>
                      <p className="text-xs text-gray-500 mt-1">
                        Uploading... {Math.round(uploadedFile.progress)}%
                      </p>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Process Button */}
      {uploadedFiles.some(file => file.status === 'success') && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 text-center"
        >
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl">
            Start Redaction Process
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default DocumentUpload;
