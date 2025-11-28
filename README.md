# Talent-Base-Service
Repositório para o serviço do Talent Base

## Pré-requisitos

- Python

## Executando

Clonar repositório

`git clone `

Criar o ambiente virtual

`python3 -m venv .venv`

Ativar o ambiente virtual

`source .venv/bin/activate`

Instalar as depedências

`pip install -r requirements.txt`

Por fim, executar

`uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`

E acessar a api em:

`localhost:8000/`

## Executando com Docker

`docker compose up --build`


## Executando testes

Para executar os testes, utilize o comando a seguir

`pyteste [path/to/file]`


Para executar testes no container de testes, utilize

`docker compose run --rm tests`

## Utilizando o Ruff

Para lint:

`ruff check`

Para formatação:

`ruff format`