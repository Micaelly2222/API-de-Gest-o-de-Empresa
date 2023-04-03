# Desafio:

# FAZER UMA API QUE RECEBA EMPRESAS E FUNCIONARIOS QUE PERTENCAM A ESSAS EMPRESAS
# 1 Salvar os dados no SQLITE ok
# 2. Usar SQL ALCHEMY ok
# 3. GET, PUT E POST
# 4. Ao cadastrar um funcionario verificar se existe a empresa associada


from typing import Optional, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///foo.db", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Organization(BaseModel):
    """Modelo de empresas"""
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), alias='_id',
                              description="Identificador da mensagem")  # Optional: não é um campo obrigatorio
    name: str
    resume: Optional[str] = None
    url: Optional[str] = None
    address: Optional[str] = None
    contacts: Optional[list[str]] = Field(default_factory=list)


class Employee(BaseModel):
    """Modelo de funcionários"""
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    address: Optional[str] = None
    organization_id: int = None


Base.metadata.create_all(engine)


# criando registros

def create_organization(db: Session, organization: Organization):
    new_organization = Organization(**organization.dict())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization


def create_employee(db: Session, employee: Employee):
    organization = db.query(Organization).filter(Organization.id == employee.organization_id).first()
    if not organization:
        raise HTTPException(status_code=401, detail="Organização não encontrada.")
    employee_dict = employee.dict(exclude={'organization_id'})
    new_employee = Employee(**employee_dict)
    new_employee.organization_id = employee.organization_id
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    new_employee.organization = organization
    return new_employee


# recupera registros

def retrieve_all_organizations(db: Session):
    return db.query(Organization).all()


def get_all_employees(db: Session):
    organizations = db.query(Organization).all()
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizações não encontradas.")
    employees = db.query(Employee).all()
    for employee in employees:
        employee.organization = next((org for org in organizations if org.id == employee.organization_id), None)
    return employees
    # estabelece a conexão com o banco de dados que é passada (via injeção de dependência) para cada função que precisa conectar ao banco.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# requisicoes

# Rota para obter todas as empresas
@app.get("/api/v1/organizations", response_model=List[Organization], status_code=status.HTTP_200_OK)
def get_all_organization(token: str, db: Session = Depends(get_db)):
    """Função para obter todas as empresas"""
    if token != "260556":  # verificando se o token é valido
        raise HTTPException(status_code=401, detail="nao autenticado")  # se for invalido vai aparecer essa exceção
    organizations = retrieve_all_organization(db)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizações não encontradas.")
    return organizations


# Rota para cadastrar uma nova empresa
@app.post("/api/v1/organizations", response_model=Organization, status_code=status.HTTP_201_CREATED)
def create_organization(token: str, organization: Organization, db: Session = Depends(get_db)):
    """Função para criar uma nova organização"""
    if token != "260556":
        raise HTTPException(status_code=401, detail="Não autenticado")
    new_organization = create_organization(db, organization)
    return new_organization


@app.put("/api/v1/organizations/", response_model=Organization, status_code=status.HTTP_200_OK)
def update_organization(token: str, organization: Organization, db: Session = Depends(get_db)):
    """Função para atualizar uma empresa"""
    if token != "260556":
        raise HTTPException(status_code=401, detail="Não autenticado")
    db_organization = get_organization(db, organization.id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    db_organization = update_organization_data(db, organization)
    return db_organization


# roda no terminal do VSCODE: uvicorn main:app --reload


@app.post("/api/v1/organizations")
async def create_organization(token: str, organization: Organization):
    """Função para criar uma nova organização"""
    if token != "260556":
        raise HTTPException(status_code=401, detail="Não autenticado")
    url = "http://localhost:8000/api/v1/organizations"
    payload = organization.dict()  # Convertendo o objeto Organization para um dicionário
    response = requests.post(url, json=payload)  # Usando o método json para enviar o dicionário como payload
    response.raise_for_status()  # Verificando se houve erro na requisição e, em caso positivo, lançando uma exceção
    return response.json()

# Bonus

# 1.Ter hierarquia entre os funcionarios, onde posso consultar toda a hierarquia de um funcionario(superiores, pares e subordinados)
# 2.Trocar para um banco de grafos (neo4j ou redis graph)
