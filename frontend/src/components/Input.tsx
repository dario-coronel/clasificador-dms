import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, ...props }) => (
  <div className="mb-4">
    {label && <label className="block text-sm font-medium text-gray-700 mb-1">{label}</label>}
    <input className="input w-full" {...props} />
    {error && <p className="text-xs text-red-600 mt-1">{error}</p>}
  </div>
);

export default Input;
