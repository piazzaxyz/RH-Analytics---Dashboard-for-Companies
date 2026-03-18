import datetime

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import Department, Employee, Position, User

# Garante criação das tabelas antes do seed
Base.metadata.create_all(bind=engine)

# Seed departamentos
with SessionLocal() as db:
    if db.query(Department).count() == 0:
        dept1 = Department(name="RH", description="Recursos Humanos")
        dept2 = Department(name="TI", description="Tecnologia da Informação")
        dept3 = Department(name="Financeiro", description="Financeiro")
        db.add_all([dept1, dept2, dept3])
        db.commit()

    # Seed cargos
    if db.query(Position).count() == 0:
        pos1 = Position(title="Analista", description="Analista RH", base_salary=3000, department_id=1)
        pos2 = Position(title="Desenvolvedor", description="Desenvolvedor TI", base_salary=4000, department_id=2)
        pos3 = Position(title="Contador", description="Contador Financeiro", base_salary=3500, department_id=3)
        db.add_all([pos1, pos2, pos3])
        db.commit()

    # Seed usuários
    if db.query(User).count() == 0:
        admin = User(
            username="admin", email="admin@empresa.com", hashed_password=get_password_hash("admin123"), role="admin"
        )
        gestor = User(
            username="gestor", email="gestor@empresa.com", hashed_password=get_password_hash("gestor123"), role="gestor"
        )
        db.add_all([admin, gestor])
        db.commit()

    # Seed funcionários
    if db.query(Employee).count() == 0:
        emp1 = Employee(
            full_name="Fulano de Tal",
            cpf="123.456.789-00",
            rg="MG-12.345.678",
            birth_date=datetime.date(1990, 1, 1),
            address="Rua A, 123",
            phone="(31) 99999-0001",
            email="fulano@empresa.com",
            work_card_number="123456",
            work_card_series="MG",
            admission_date=datetime.date(2020, 1, 1),
            dismissal_date=None,
            status="ativo",
            department_id=1,
            position_id=1,
            supervisor_id=None,
            bank_name="Banco A",
            bank_agency="0001",
            bank_account="12345-6",
            bank_account_type="corrente",
            photo_blob=None,
            salary=3000.0,
            pis_pasep="12345678901",
        )
        emp2 = Employee(
            full_name="Ciclano Silva",
            cpf="987.654.321-00",
            rg="MG-87.654.321",
            birth_date=datetime.date(1985, 5, 10),
            address="Rua B, 456",
            phone="(31) 99999-0002",
            email="ciclano@empresa.com",
            work_card_number="654321",
            work_card_series="MG",
            admission_date=datetime.date(2019, 5, 10),
            dismissal_date=None,
            status="ativo",
            department_id=2,
            position_id=2,
            supervisor_id=None,
            bank_name="Banco B",
            bank_agency="0002",
            bank_account="65432-1",
            bank_account_type="corrente",
            photo_blob=None,
            salary=4000.0,
            pis_pasep="10987654321",
        )
        emp3 = Employee(
            full_name="Beltrano Souza",
            cpf="111.222.333-44",
            rg="MG-11.223.344",
            birth_date=datetime.date(1980, 12, 20),
            address="Rua C, 789",
            phone="(31) 99999-0003",
            email="beltrano@empresa.com",
            work_card_number="112233",
            work_card_series="MG",
            admission_date=datetime.date(2018, 12, 20),
            dismissal_date=None,
            status="ativo",
            department_id=3,
            position_id=3,
            supervisor_id=None,
            bank_name="Banco C",
            bank_agency="0003",
            bank_account="11223-3",
            bank_account_type="corrente",
            photo_blob=None,
            salary=3500.0,
            pis_pasep="11223344556",
        )
        db.add_all([emp1, emp2, emp3])
        db.commit()
