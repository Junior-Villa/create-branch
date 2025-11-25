🚀 Automação de Criação de Branches via Webhook

Este projeto automatiza a criação de branches em múltiplos repositórios do GitHub com base nos dados recebidos por um webhook (como Jira ou outras ferramentas de gestão).
O objetivo é agilizar o início do desenvolvimento e padronizar o fluxo entre equipes e serviços.

🧠 Como funciona

Uma issue é atualizada e dispara um webhook.

O serviço recebe os dados (branch base, labels, chave da issue).

O label informa qual repositório deve receber a nova branch.

A API busca o último commit da branch base.

Uma nova branch é criada automaticamente no GitHub.

🛠 Tecnologias utilizadas

Python + Flask

GitHub REST API

Requests

Flask-CORS

⚙️ Configuração
Variáveis de ambiente
GITHUB_OWNER=seu-usuario-ou-organizacao
GITHUB_TOKEN=seu-token-github

Instale as dependências
pip install flask flask-cors requests

Execute o serviço
python app.py


A rota principal é:

POST /webhook

📦 Exemplo de Payload
{
  "issue": {
    "key": "TASK-123",
    "source_branch": "main",
    "labels": ["PROJECT_BACKEND"]
  }
}

🧩 Personalização

Você define no código qual label cria branch em qual repositório:

LABEL_TO_REPO = {
    "PROJECT_BACKEND": "backend-service",
    "PROJECT_FRONTEND": "frontend-app",
    "PROJECT_MOBILE": "mobile-flutter"
}


Basta ajustar conforme sua estrutura.

📌 Resultado da API
{
  "message": "Processamento concluído",
  "details": [
    {
      "repo": "backend-service",
      "result": "Branch criada com sucesso"
    }
  ]
}