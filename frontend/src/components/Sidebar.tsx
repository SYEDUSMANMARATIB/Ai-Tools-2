import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Upload,
  Clock,
  FileText,
  BarChart3,
  Shield,
  Settings,
  HelpCircle,
  Home
} from 'lucide-react';

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<any>;
  badge?: string;
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Upload Documents', href: '/upload', icon: Upload },
  { name: 'Processing Status', href: '/processing', icon: Clock, badge: '2' },
  { name: 'Results', href: '/results', icon: FileText },
  { name: 'Audit Dashboard', href: '/audit', icon: BarChart3 },
  { name: 'Security Settings', href: '/settings', icon: Shield },
  { name: 'System Settings', href: '/system', icon: Settings },
  { name: 'Help & Support', href: '/help', icon: HelpCircle },
];

const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <motion.div
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg border-r border-gray-200"
    >
      <div className="flex flex-col h-full">
        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            const Icon = item.icon;

            return (
              <Link key={item.name} to={item.href}>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`
                    group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200
                    ${isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  <Icon
                    className={`
                      mr-3 h-5 w-5 transition-colors
                      ${isActive ? 'text-blue-700' : 'text-gray-400 group-hover:text-gray-500'}
                    `}
                  />
                  <span className="flex-1">{item.name}</span>
                  {item.badge && (
                    <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      {item.badge}
                    </span>
                  )}
                </motion.div>
              </Link>
            );
          })}
        </nav>

        {/* Stats Section */}
        <div className="px-4 py-6 border-t border-gray-200">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4">
            <h3 className="text-sm font-medium text-gray-900 mb-3">
              Today's Activity
            </h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Documents Processed</span>
                <span className="font-medium text-gray-900">24</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Items Redacted</span>
                <span className="font-medium text-gray-900">156</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Success Rate</span>
                <span className="font-medium text-green-600">98.5%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-4 border-t border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="h-8 w-8 bg-blue-600 rounded-full flex items-center justify-center">
              <Shield className="h-4 w-4 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                Redaction Tool v1.0
              </p>
              <p className="text-xs text-gray-500">
                Secure & Compliant
              </p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default Sidebar;
