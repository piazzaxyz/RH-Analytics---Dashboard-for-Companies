import React, { useState, useEffect } from 'react';
import { Upload, Loader2, Clock } from 'lucide-react';
import Button from '../components/ui/Button';
import DataCard from '../components/ui/DataCard';
import { fetchTimesheets, importTimesheet } from '../services/timesheet';
import './TimesheetsPage.css';

const TimesheetsPage: React.FC = () => {
  const [timesheets, setTimesheets] = useState<any[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [importing, setImporting] = useState(false);

  useEffect(() => {
    fetchTimesheets()
      .then(setTimesheets)
      .finally(() => setLoading(false));
  }, []);

  const handleImport = async () => {
    if (!file) return;
    setImporting(true);
    try {
      await importTimesheet(file);
      const data = await fetchTimesheets();
      setTimesheets(data);
      setFile(null);
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="timesheets-page">
      <header className="page-header">
        <div>
          <h1>Ponto e Jornada</h1>
          <p className="page-subtitle">Registros de ponto e importação</p>
        </div>
        <div className="import-actions">
          <label className="file-input-label">
            <input
              type="file"
              accept=".csv,.json,.pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              style={{ display: 'none' }}
            />
            <span className="btn btn--secondary">
              <Upload size={18} />
              {file ? file.name : 'Selecionar arquivo'}
            </span>
          </label>
          <Button
            onClick={handleImport}
            disabled={!file || importing}
            loading={importing}
            icon={Upload}
          >
            Importar
          </Button>
        </div>
      </header>

      <DataCard title="Registros de Ponto">
        {loading ? (
          <div className="table-loading">
            <Loader2 size={32} className="spin" />
            <p>Carregando...</p>
          </div>
        ) : (
          <div className="timesheets-grid">
            {timesheets.map((t) => (
              <div key={t.id} className="timesheet-card">
                <div className="timesheet-card__icon">
                  <Clock size={20} />
                </div>
                <div className="timesheet-card__content">
                  <span className="timesheet-card__emp">Colaborador #{t.employee_id}</span>
                  <span className="timesheet-card__date">{t.date}</span>
                  <div className="timesheet-card__times">
                    <span>Entrada: {t.clock_in || '-'}</span>
                    <span>Saída: {t.clock_out || '-'}</span>
                  </div>
                  <span className="timesheet-card__total">{t.total_minutes} min</span>
                </div>
                <span className={`status-badge status-${t.status}`}>{t.status}</span>
              </div>
            ))}
            {!timesheets.length && (
              <p className="empty-state">Nenhum registro de ponto. Importe um arquivo CSV.</p>
            )}
          </div>
        )}
      </DataCard>
    </div>
  );
};

export default TimesheetsPage;
