# Tech Agent Production Starter

---

## 🚀 Deploy to GKE (Standard Cluster) via GitHub Actions

This section covers the complete setup to deploy the agent to a **Google Kubernetes Engine Standard cluster** with a ReplicaSet (min 2 replicas), automatic scaling, and a full **GitHub Actions CI/CD pipeline**.

---

### Prerequisites

| Tool | Purpose |
|------|---------|
| `gcloud` CLI | GCP project setup |
| `kubectl` | Kubernetes management |
| `docker` | Local image builds (optional) |
| GitHub repo with Actions enabled | CI/CD |

---

### Step 1 — GCP Project Setup

```bash
export PROJECT_ID=your-gcp-project-id
export REGION=australia-southeast1
export ZONE=australia-southeast1-a
export CLUSTER_NAME=tech-agent-cluster
export AR_REPO=tech-agent
export GCP_SA_NAME=tech-agent-sa

gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  container.googleapis.com \
  artifactregistry.googleapis.com \
  iam.googleapis.com \
  iamcredentials.googleapis.com
```

---

### Step 2 — Create Artifact Registry Repository

```bash
gcloud artifacts repositories create $AR_REPO \
  --repository-format=docker \
  --location=$REGION \
  --description="Tech Agent Docker images"
```

---

### Step 3 — Create GKE Standard Cluster

```bash
gcloud container clusters create $CLUSTER_NAME \
  --zone=$ZONE \
  --num-nodes=2 \
  --machine-type=e2-standard-2 \
  --enable-autoscaling --min-nodes=2 --max-nodes=5 \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --release-channel=regular
```

> **Workload Identity** (`--workload-pool`) is required for the pod to call Google APIs securely without embedding keys in the image.

---

### Step 4 — Create GCP Service Account & IAM Bindings

```bash
# Create a dedicated GCP service account for the agent
gcloud iam service-accounts create $GCP_SA_NAME \
  --display-name="Tech Agent GKE SA"

# Grant it access to Gemini / Vertex AI
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${GCP_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"

# Allow the Kubernetes ServiceAccount to impersonate the GCP SA (Workload Identity)
gcloud iam service-accounts add-iam-policy-binding \
  ${GCP_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[default/tech-agent-ksa]"

# Update the annotation in k8s/serviceaccount.yaml
sed -i "s|GCP_SA_NAME@PROJECT_ID|${GCP_SA_NAME}@${PROJECT_ID}|g" k8s/serviceaccount.yaml
```

---

### Step 5 — Store Secrets in Kubernetes

```bash
# Get credentials for your cluster
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE

# Create the secret (replace values with your real keys)
kubectl create secret generic tech-agent-secrets \
  --from-literal=GOOGLE_API_KEY= \
  --from-literal=BRAVE_API_KEY=
```

---

### Step 6 — Configure GitHub Actions Workload Identity Federation

This lets GitHub Actions authenticate to GCP **without storing long-lived credentials**.

```bash
# Create a Workload Identity Pool
gcloud iam workload-identity-pools create github-pool \
  --location=global \
  --display-name="GitHub Actions Pool"

# Create an OIDC provider for GitHub
gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location=global \
  --workload-identity-pool=github-pool \
  --display-name="GitHub OIDC" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="attribute.repository=='********
# Get the full provider name
PROVIDER=$(gcloud iam workload-identity-pools providers describe github-provider \
  --location=global \
  --workload-identity-pool=github-pool \
  --format="value(name)")

# Allow GitHub Actions to impersonate the GCP SA
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud iam service-accounts add-iam-policy-binding \
  ${GCP_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/repo name/"

echo "Workload Identity Provider: ${PROVIDER}"
echo "Service Account: ${GCP_SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
```

---

### Step 7 — Set GitHub Repository Secrets

In your GitHub repo → **Settings → Secrets and variables → Actions**, add:

| Secret name | Value |
|-------------|-------|
| `GCP_PROJECT_ID` | Your GCP project ID |
| `GKE_CLUSTER_NAME` | `tech-agent-cluster` |
| `GKE_CLUSTER_ZONE` | e.g. `australia-southeast1-a` |
| `GCP_REGION` | e.g. `australia-southeast1` |
| `GCP_WORKLOAD_IDENTITY_PROVIDER` | Full provider name from Step 6 |
| `GCP_SERVICE_ACCOUNT` | `tech-agent-sa@YOUR_PROJECT.iam.gserviceaccount.com` |

---

### Step 8 — Deploy

Push to `main` — the pipeline runs automatically:

```
push to main
  └─► Lint & Test
        └─► Build Docker image
              └─► Push to Artifact Registry
                    └─► kubectl apply (Deployment + Service + Ingress + HPA)
                          └─► kubectl rollout status
```

Or trigger manually from **Actions → Deploy to GKE → Run workflow**.

---

### Kubernetes Resources Created

| Resource | File | Purpose |
|----------|------|---------|
| `Deployment` | `k8s/deployment.yaml` | ReplicaSet, rolling updates, health probes |
| `Service` | `k8s/service.yaml` | Internal ClusterIP routing |
| `Ingress` | `k8s/ingress.yaml` | GCE L7 load balancer (public HTTP) |
| `ServiceAccount` | `k8s/serviceaccount.yaml` | Workload Identity binding |
| `HPA` | `k8s/hpa.yaml` | Auto-scale 2–10 pods on CPU/memory |

---

### Verify the Deployment

```bash
# Check pods
kubectl get pods -l app=tech-agent

# Check replica set
kubectl get rs -l app=tech-agent

# Check HPA
kubectl get hpa tech-agent-hpa

# Get public IP
kubectl get ingress tech-agent

# View logs
kubectl logs -l app=tech-agent --tail=50 -f
```

---

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
