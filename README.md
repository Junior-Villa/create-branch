Automação de Criação de Branches via Webhook

Este projeto recebe webhooks de ferramentas externas (como Jira) e cria automaticamente branches em repositórios do GitHub, de acordo com os labels definidos em cada issue. A ideia é agilizar o início do desenvolvimento e evitar trabalho repetitivo.

Como funciona

O webhook envia os dados da issue.

A API identifica quais repositórios devem ser atualizados com base nos labels.

Ela consulta o último commit da branch base e cria uma nova branch no GitHub.

Simples e flexível para quem trabalha com vários serviços ao mesmo tempo.

Tecnologias

Python + Flask

GitHub REST API

Requests

Configuração

Defina as variáveis de ambiente:

GITHUB_OWNER=seu-usuario-ou-org
GITHUB_TOKEN=seu-token-aqui


Instale as dependências:

pip install flask flask-cors requests


Execute:

python app.py


A rota principal é:

POST /webhook

Exemplo de payload
{
  "issue": {
    "key": "TASK-123",
    "source_branch": "main",
    "labels": ["PROJECT_BACKEND"]
  }
}

Personalização

No código existe um dicionário simples onde você define a relação entre labels e repositórios:

LABEL_TO_REPO = {
    "PROJECT_BACKEND": "backend-service",
    "PROJECT_FRONTEND": "frontend-app"
}
