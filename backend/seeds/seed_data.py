#!/usr/bin/env python3
"""Seed data para o sistema RH - 15 colaboradores, usuários, departamentos, cargos."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime, time
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.department import Department
from app.models.position import Position
from app.models.employee import Employee, EmployeeStatus
from app.models.timesheet import Timesheet, TimesheetStatus
from app.models.payroll import Payroll, PayrollStatus

import app.models.audit
import app.models.course
import app.models.document
import app.models.evaluation
import app.models.loan
import app.models.loan_installment
import app.models.position_history
import app.models.timesheet_import


def gerar_cpf_valido(base: int) -> str:
    """Gera CPF válido a partir de base de 9 dígitos."""
    base_str = str(base).zfill(9)
    if len(base_str) > 9:
        base_str = base_str[:9]
    digits = [int(d) for d in base_str]
    s1 = sum(digits[i] * (10 - i) for i in range(9))
    d1 = 0 if s1 % 11 < 2 else 11 - (s1 % 11)
    digits.append(d1)
    s2 = sum(digits[i] * (11 - i) for i in range(10))
    d2 = 0 if s2 % 11 < 2 else 11 - (s2 % 11)
    digits.append(d2)
    return "".join(map(str, digits))


def run_seed_minimal():
    """Cria apenas usuários, departamentos e cargos - sem colaboradores."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        users_data = [
            ("admin@rh.com", "admin123", UserRole.admin),
            ("rh@rh.com", "rh123", UserRole.rh),
            ("gestor@rh.com", "gestor123", UserRole.gestor),
            ("visualizador@rh.com", "vis123", UserRole.visualizador),
        ]
        for email, pwd, role in users_data:
            if db.query(User).filter(User.email == email).first():
                continue
            u = User(username=email, email=email, hashed_password=get_password_hash(pwd), role=role)
            db.add(u)
        db.commit()

        if db.query(Department).count() == 0:
            depts = [
                Department(name="TI", description="Tecnologia da Informação"),
                Department(name="RH", description="Recursos Humanos"),
                Department(name="Financeiro", description="Financeiro e Contábil"),
                Department(name="Comercial", description="Vendas e Marketing"),
                Department(name="Operações", description="Operações e Logística"),
            ]
            for d in depts:
                db.add(d)
            db.commit()

        if db.query(Position).count() == 0:
            positions = [
                Position(title="Desenvolvedor", description="Desenvolvedor de Software", base_salary=6500, department_id=1),
                Position(title="Analista RH", description="Analista de RH", base_salary=4500, department_id=2),
                Position(title="Contador", description="Contador", base_salary=5500, department_id=3),
                Position(title="Vendedor", description="Representante Comercial", base_salary=4000, department_id=4),
                Position(title="Coordenador", description="Coordenador de Operações", base_salary=6000, department_id=5),
            ]
            for p in positions:
                db.add(p)
            db.commit()

        print(f"Seed mínimo: {db.query(User).count()} usuários, {db.query(Department).count()} departamentos, {db.query(Position).count()} cargos.")
    finally:
        db.close()


def run_seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            print("Dados já existem. Execute 'python seeds/reset_data.py' para zerar primeiro.")
            return

        users_data = [
            ("admin@rh.com", "admin123", UserRole.admin),
            ("rh@rh.com", "rh123", UserRole.rh),
            ("gestor@rh.com", "gestor123", UserRole.gestor),
            ("visualizador@rh.com", "vis123", UserRole.visualizador),
        ]
        for email, pwd, role in users_data:
            u = User(username=email, email=email, hashed_password=get_password_hash(pwd), role=role)
            db.add(u)
        db.commit()

        depts = [
            Department(name="TI", description="Tecnologia da Informação"),
            Department(name="RH", description="Recursos Humanos"),
            Department(name="Financeiro", description="Financeiro e Contábil"),
            Department(name="Comercial", description="Vendas e Marketing"),
            Department(name="Operações", description="Operações e Logística"),
        ]
        for d in depts:
            db.add(d)
        db.commit()

        positions = [
            Position(title="Desenvolvedor", description="Desenvolvedor de Software", base_salary=6500, department_id=1),
            Position(title="Analista RH", description="Analista de RH", base_salary=4500, department_id=2),
            Position(title="Contador", description="Contador", base_salary=5500, department_id=3),
            Position(title="Vendedor", description="Representante Comercial", base_salary=4000, department_id=4),
            Position(title="Coordenador", description="Coordenador de Operações", base_salary=6000, department_id=5),
        ]
        for p in positions:
            db.add(p)
        db.commit()

        nomes = [
            "Ana Silva", "Bruno Santos", "Carla Oliveira", "Diego Costa", "Elena Ferreira",
            "Fernando Lima", "Gabriela Souza", "Henrique Alves", "Isabela Martins", "João Pereira",
            "Karina Rocha", "Lucas Mendes", "Mariana Dias", "Nicolas Barbosa", "Patricia Nunes"
        ]
        for i, nome in enumerate(nomes):
            dept_id = (i % 5) + 1
            pos_id = (i % 5) + 1
            cpf = gerar_cpf_valido(100000000 + i)
            emp = Employee(
                full_name=nome,
                cpf=cpf,
                rg=f"12.345.67{i}-X",
                birth_date=date(1985 + (i % 15), (i % 12) + 1, 15),
                address=f"Rua Exemplo {i+1}, Centro",
                phone=f"1198765{i:04d}",
                email=nome.lower().replace(" ", ".") + "@empresa.com",
                work_card_number=f"001{i:05d}",
                work_card_series="1234",
                admission_date=date(2020 + (i % 4), 1, 1 + (i % 28)),
                status=EmployeeStatus.ativo,
                department_id=dept_id,
                position_id=pos_id,
                bank_name="Banco do Brasil",
                bank_agency="1234",
                bank_account=f"12345-{i}",
                bank_account_type="corrente",
                salary=4000 + (i * 200),
                pis_pasep=f"123.45678.90-{i}"
            )
            db.add(emp)
        db.commit()

        employees = db.query(Employee).all()
        ref_month = datetime.now().strftime("%Y-%m")
        for emp in employees[:10]:
            for day in range(1, 21):
                ts = Timesheet(
                    employee_id=emp.id,
                    date=date(int(ref_month[:4]), int(ref_month[5:7]), day),
                    clock_in=time(8, 0),
                    clock_out=time(12, 0),
                    clock_in_2=time(13, 0),
                    clock_out_2=time(17, 0),
                    total_minutes=480,
                    overtime_50_minutes=0,
                    overtime_100_minutes=0,
                    night_shift_minutes=0,
                    status=TimesheetStatus.ok
                )
                db.add(ts)
        db.commit()

        for emp in employees[:5]:
            payroll = Payroll(
                employee_id=emp.id,
                reference_month=ref_month,
                base_salary=emp.salary,
                overtime_50_value=0,
                overtime_100_value=0,
                night_additional_value=0,
                dsr_value=0,
                bonus_value=0,
                hazard_pay=0,
                unhealthy_pay=0,
                gross_salary=emp.salary,
                inss_value=min(emp.salary * 0.11, 908.85),
                irrf_value=0,
                vt_discount=0,
                vr_discount=0,
                health_plan_discount=0,
                loan_discount=0,
                absence_discount=0,
                alimony_discount=0,
                other_discounts=0,
                net_salary=emp.salary * 0.85,
                status=PayrollStatus.processado,
                processed_at=datetime.now()
            )
            db.add(payroll)
        db.commit()

        print(f"Seed concluído: {db.query(User).count()} usuários, {db.query(Department).count()} departamentos,")
        print(f"{db.query(Position).count()} cargos, {db.query(Employee).count()} colaboradores,")
        print(f"{db.query(Timesheet).count()} registros de ponto, {db.query(Payroll).count()} folhas.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
