import React, { type ButtonHTMLAttributes } from 'react';

export interface SakinahButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  fullWidth?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export const SakinahButton: React.FC<SakinahButtonProps> = ({
  children,
  variant = 'primary',
  fullWidth = true,
  size = 'md',
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = "inline-flex items-center justify-center font-serif font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[#07090f] disabled:opacity-50 disabled:cursor-not-allowed";
  
  const sizeStyles = {
    sm: "py-[10px] px-4 text-[14px] rounded-[10px]",
    md: "py-[14px] px-6 text-[16px] rounded-[14px]",
    lg: "py-[16px] px-8 text-[20px] rounded-[14px]"
  };

  const variantStyles = {
    primary: "bg-[#D4A853] text-[#07090f] hover:bg-[#ebd097] focus:ring-[#D4A853]",
    secondary: "bg-transparent border border-[#D4A853] text-[#D4A853] hover:bg-[rgba(212,168,83,0.1)] focus:ring-[#D4A853]",
    danger: "bg-transparent border border-[rgba(201,138,138,0.3)] text-[#C98A8A] font-sans hover:bg-[rgba(201,138,138,0.1)] focus:ring-[#C98A8A]",
    ghost: "bg-transparent text-[#9aa0ac] hover:text-[#EDE7DA] focus:ring-[#D4A853]"
  };

  const widthStyle = fullWidth ? "w-full" : "";

  return (
    <button
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${widthStyle} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
