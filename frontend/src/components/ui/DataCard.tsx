import React from 'react';
import './DataCard.css';

interface DataCardProps {
  title: string;
  children: React.ReactNode;
  action?: React.ReactNode;
}

const DataCard: React.FC<DataCardProps> = ({ title, children, action }) => (
  <div className="data-card">
    <div className="data-card__header">
      <h3 className="data-card__title">{title}</h3>
      {action && <div className="data-card__action">{action}</div>}
    </div>
    <div className="data-card__body">{children}</div>
  </div>
);

export default DataCard;
