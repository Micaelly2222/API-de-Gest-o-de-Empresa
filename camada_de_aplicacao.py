from fastapi import FastAPI, HTTPException, status, Depends

Base.metadata.create_all(engine)

app = FastAPI()


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
    response.raise_for_status()  # Verificando se houve erro na requisição
    return response.json()
