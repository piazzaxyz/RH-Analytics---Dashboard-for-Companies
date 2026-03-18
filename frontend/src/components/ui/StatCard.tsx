import React from 'react';
import { LucideIcon } from 'lucide-react';
import './StatCard.css';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: { value: number; label: string };
  accent?: 'blue' | 'green' | 'amber' | 'violet';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon: Icon, trend, accent = 'blue' }) => (
  <div className={`stat-card stat-card--${accent}`}>
    <div className="stat-card__icon">
      <Icon size={24} />
    </div>
    <div className="stat-card__content">
      <span className="stat-card__title">{title}</span>
      <span className="stat-card__value">{value}</span>
      {trend && (
        <span className={`stat-card__trend ${trend.value >= 0 ? 'positive' : 'negative'}`}>
          {trend.value >= 0 ? '+' : ''}{trend.value}% {trend.label}
        </span>
      )}
    </div>
  </div>
);

export default StatCard;
