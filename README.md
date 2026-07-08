# Tech Agent Production Starter

Production-style Python Google ADK multi-agent repository for technical learning, DevOps, Cloud, Kubernetes, Terraform, GCP, AWS, APIs, CI/CD, MCP, and code examples.

## Local setup

```bash
cd tech-agent-production-fixed
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
MODEL=gemini-1.5-flash
GOOGLE_API_KEY=your_google_ai_studio_api_key
```

Run:

```bash
export PYTHONPATH=.
adk web tech_agent
```

## Cloud Run

```bash
export PROJECT_ID=your-gcp-project
export REGION=australia-southeast1
export SERVICE=tech-agent-production
./scripts/deploy_cloud_run.sh
```

## Architecture

- planner_agent
- researcher_agent
- writer_agent
- reviewer_agent
- blogger_agent
- diagram_agent
- quiz_agent

MCP servers:

- search_server.py
- docs_server.py
- github_server.py
- trends_server.py
- code_examples_server.py
- kubernetes_server.py
- terraform_server.py
- aws_server.py
- gcp_server.py
- devops_server.py
