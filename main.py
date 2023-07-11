from typing import List

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from CRUD import create_organization, retrieve_all_organizations, get_organization, update_organization_data
from Models import Organization
from camada_de_banco import get_db

app = FastAPI()

# Rota para obter todas as empresas
@app.get("/api/v1/organizations", response_model=List[Organization], status_code=status.HTTP_200_OK)
def get_all_organization(db: Session = Depends(get_db)):
    organizations = retrieve_all_organizations(db)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizações não encontradas.")
    return organizations


# Rota para cadastrar uma nova empresa
@app.post("/api/v1/organizations", response_model=Organization, status_code=status.HTTP_201_CREATED)
def create_new_organization(organization: Organization, db: Session = Depends(get_db)):
    new_organization = create_organization(db, organization)
    return new_organization


# Rota para atualizar uma empresa
@app.put("/api/v1/organizations/", response_model=Organization, status_code=status.HTTP_200_OK)
def update_organization(organization: Organization, db: Session = Depends(get_db)):
    db_organization = get_organization(db, organization.id)
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organização não encontrada")
    db_organization = update_organization_data(db, organization)
    return db_organization
