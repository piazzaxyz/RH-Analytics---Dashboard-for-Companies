#!/usr/bin/env python3
"""Zera todos os dados. Remove o banco e executa seed mínimo (apenas usuários, departamentos, cargos).
Pare o servidor backend antes de executar, ou o script usará DELETE nas tabelas."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.core.database import engine, SessionLocal, Base
from app.core.config import Settings

import app.models.audit
import app.models.course
import app.models.document
import app.models.evaluation
import app.models.loan
import app.models.loan_installment
import app.models.payroll
import app.models.position_history
import app.models.timesheet
import app.models.timesheet_import
import app.models.employee
import app.models.department
import app.models.ala
import app.models.position
import app.models.user


def run_reset():
    try:
        db_path = Settings().DATABASE_URL.replace("sqlite:///", "").replace("sqlite:////", "")
        if db_path.startswith("./"):
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), db_path[2:])
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"Banco removido: {db_path}")
    except PermissionError:
        print("Banco em uso. Zerando tabelas com DELETE...")
        with engine.connect() as conn:
            for table in ["audit_logs", "loan_installments", "loans", "evaluations", "documents",
                          "courses", "positions_history", "timesheet_imports", "timesheets",
                          "payrolls", "employees", "positions", "alas", "departments", "users"]:
                try:
                    conn.execute(text(f"DELETE FROM {table}"))
                    conn.commit()
                except Exception:
                    pass

    Base.metadata.create_all(bind=engine)
    print("Executando seed mínimo (usuários, departamentos, cargos)...")
    from seeds.seed_data import run_seed_minimal
    run_seed_minimal()
    print("Pronto! Banco zerado. Use admin@rh.com / admin123 para login.")


if __name__ == "__main__":
    run_reset()
