import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'outline' | 'danger';
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, ...props }) => {
  const base = 'px-4 py-2 rounded-lg font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500';
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    outline: 'bg-white border border-primary-600 text-primary-600 hover:bg-primary-50',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  };
  return (
    <button className={`${base} ${variants[variant]}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
