import React from 'react';

const variants = {
  primary: 'bg-gradient-to-r from-[#3366FF] to-[#8A2BE2] text-white hover:opacity-90',
  secondary: 'bg-[#353d47] text-white hover:bg-[#424d5a]',
  outline: 'border border-[#3366FF] text-[#3366FF] hover:bg-[#3366FF]/10',
  ghost: 'text-[#e0e0e0] hover:bg-[#353d47]',
  danger: 'bg-[#ff6b6b] text-white hover:bg-[#ff5252]',
};

const sizes = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

export function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  disabled = false,
  ...props 
}) {
  return (
    <button
      className={`
        inline-flex items-center justify-center gap-2 font-medium rounded-lg
        transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed
        ${variants[variant] || variants.primary}
        ${sizes[size] || sizes.md}
        ${className}
      `}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
