import React from 'react';

export function Card({ children, className = '', ...props }) {
  return (
    <div 
      className={`bg-[#242930] border border-[#2d333b] rounded-xl overflow-hidden ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '', ...props }) {
  return (
    <div 
      className={`px-5 py-4 border-b border-[#2d333b] ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardBody({ children, className = '', ...props }) {
  return (
    <div className={`p-5 ${className}`} {...props}>
      {children}
    </div>
  );
}

export default Card;
