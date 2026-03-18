import React from 'react';
import { LucideIcon } from 'lucide-react';
import './Button.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  icon?: LucideIcon;
  loading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon: Icon,
  loading,
  disabled,
  className = '',
  ...props
}) => (
  <button
    className={`btn btn--${variant} btn--${size} ${className}`}
    disabled={disabled || loading}
    {...props}
  >
    {loading ? (
      <span className="btn__spinner" />
    ) : Icon ? (
      <>
        <Icon size={size === 'sm' ? 16 : 20} />
        {children}
      </>
    ) : (
      children
    )}
  </button>
);

export default Button;
