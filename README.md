# API de Gestão de Empresa

Fazer uma API que receba empresas e funcionarios que pertencam a essas empresas


Essa API permite gerenciar empresas e funcionários associados a elas. É possível realizar operações de criação, leitura e atualização dos dados. A API armazena os dados em um banco de dados SQLite e utiliza o SQL Alchemy como ferramenta ORM para lidar com as consultas e operações no banco de dados.

- [x] Salvar os dados no SQLITE
- [x] Usar SQL ALCHEMY
- [x] GET, PUT E POST
- [x] Ao cadastrar um funcionario verificar se existe a empresa associada

## Bonus

- [ ] Ter hierarquia entre os funcionarios, onde posso consultar toda a hierarquia de um funcionario(superiores, pares e
  subordinados) :cry:
- [ ] Trocar para um banco de grafos (neo4j ou redis graph)

## Linguagens e Ferramentas Utilizadas

* [Python](https://docs.python.org/pt-br/3/tutorial/), linguagem de programação de alto nível
* [SqlAlchemy](https://www.sqlalchemy.org/), ferramentas SQL em Python para ORM flexíveis
* [FastAPI](https://fastapi.tiangolo.com/), framework Python focado no desenvolvimento de API's
* [Unittest](https://docs.python.org/3/library/unittest.html), biblioteca de testes unitários em Python. Utilizada para escrever e executar testes automatizados.

## Testes Automatizados

O projeto inclui testes automatizados implementados com o uso da biblioteca `unittest`. Os testes garantem o correto funcionamento das funcionalidades principais da API.
