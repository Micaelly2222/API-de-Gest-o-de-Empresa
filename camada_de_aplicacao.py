import logging

from fastapi import FastAPI, HTTPException, status

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
