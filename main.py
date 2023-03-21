# Desafio:

# FAZER UMA API QUE RECEBA EMPRESAS E FUNCIONARIOS QUE PERTENCAM A ESSAS EMPRESAS
# 1 Salvar os dados no SQLITE ok
# 2. Usar SQL ALCHEMY ok
# 3. GET, PUT E POST
# 4. Ao cadastrar um funcionario verificar se existe a empresa associada


import logging
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
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
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# recupera registros

def retrieve_all_organization(db: Session):
    return db.query(Organization).all()


def get_all_employees(db: Session):
    return db.query(Employee).all()

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
@app.get("/api/v1/organizations", response_model=Organization, status_code=status.HTTP_200_OK)
def get_all_organization(token: str, organization: Organization):
    """Função para obter todas as empresas"""
    if token != "260556":  # verificando se o token é valido
        raise HTTPException(status_code=401, detail="nao autenticado")  # se for invalido vai aparecer essa exceção
        logging.error('nao autenticado')
        organizations = retrieve_all_organization(db)
    if not organizations:
        raise HTTPException(status_code=401, detail="Organização não encontrada.")
        logging.error('Organização não encontrada.')
    return organizations


# Rota para cadastrar uma nova empresa
@app.post("/api/v1/organizations", response_model=Organization,
          status_code=status.HTTP_200_OK)  # rota da API, responsável por realizar o cadastro de novas organizacoes, com a requisição do tipo POST
async def create_organization(token: str, organization: Organization):
    """Função para criar uma empresa"""
    if token != "260556":  # verificando se o token é valido
        raise HTTPException(status_code=401, detail="nao autenticado")  # se for invalido vai aparecer essa exceção
        logging.error('nao autenticado')
    ok  # TODO printar a mensagem recebida usando [logger](https://docs.python.org/3/library/logging.html)
    return organization  # retorna a organizacao criada


@app.put("/api/v1/organizations/", response_model=Organization, status_code=status.HTTP_200_OK)
def update_organization(token: str, organization: Organization):
    """Função para atualizar as empresas"""
    if token != "260556":  # verificando se o token é valido
        raise HTTPException(status_code=401, detail="nao autenticado")  # se for invalido vai aparecer essa exceção
        logging.error('nao autenticado')
    organizations = retrieve_all_organization(db)
    if not organizations:
        raise HTTPException(status_code=401, detail="Organização não encontrada.")
        logging.error('Organização não encontrada.')
    db_organization = update_organization_data(db, organization)
    return organizations


# roda no terminal do VSCODE: uvicorn main:app --reload


@app.post("/api/v1/organizations")
async def request(token: str, organization: Organization):
    if token != "260556":
        raise HTTPException(status_code=401, detail="nao autenticado")
        logging.error('nao autenticado')
    url = "http://localhost:8000/api/v1/organizations"
    payload = {
        "id": organization.id,
        "name": organization.name,
        "address": organization.address,
    }
    response = requests.post(url, data=json.dumps(payload))
    return response.json()

# Bonus

# 1.Ter hierarquia entre os funcionarios, onde posso consultar toda a hierarquia de um funcionario(superiores, pares e subordinados)
# 2.Trocar para um banco de grafos (neo4j ou redis graph)
