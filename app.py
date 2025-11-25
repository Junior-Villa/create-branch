from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Mapeamento entre labels e repositórios
# (Pode ser público — não contém dados sensíveis)
LABEL_TO_REPO = {
    "PROJECT_BACKEND": "backend-service",
    "PROJECT_FRONTEND": "frontend-app",
    "PROJECT_MOBILE": "mobile-flutter",
}

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Webhook que recebe dados de uma Issue (por exemplo, do Jira)
    e cria branches automaticamente nos repositórios GitHub.
    """
    data = request.json
    issue_data = data.get('issue')

    if not issue_data:
        return jsonify({'error': 'Issue data not provided'}), 400

    issue_key = issue_data.get('key')            # Nome da nova branch
    source_branch = issue_data.get('source_branch')  # Branch base (ex: "main")
    issue_labels = issue_data.get('labels', [])

    if not issue_key or not source_branch:
        return jsonify({'error': 'Missing required fields'}), 400

    # Credenciais via variáveis de ambiente (seguro para código público)
    github_owner = os.environ.get("GITHUB_OWNER")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_owner or not github_token:
        return jsonify({'error': 'GitHub credentials not configured'}), 500

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    results = []

    # Processa cada label da issue
    for label in issue_labels:
        if label in LABEL_TO_REPO:
            repo = LABEL_TO_REPO[label]
            result = create_branch(repo, issue_key, source_branch, github_owner, headers)
            results.append({ "repo": repo, "result": result })

    return jsonify({ "message": "Processamento concluído", "details": results }), 201


def get_last_commit_sha(repo, branch, owner, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return None

    return res.json()["commit"]["sha"]


def create_branch(repo, new_branch, source_branch, owner, headers):
    sha = get_last_commit_sha(repo, source_branch, owner, headers)
    if sha is None:
        return "Erro ao buscar commit base"

    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": sha
    }

    url = f"https://api.github.com/repos/{owner}/{repo}/git/refs"
    res = requests.post(url, headers=headers, json=payload)

    if res.status_code == 201:
        return "Branch criada com sucesso"
    else:
        return f"Falhou: {res.text}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
