#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-your-gcp-project}"
REGION="${REGION:-australia-southeast1}"
SERVICE="${SERVICE:-tech-agent-production}"
MODEL="${MODEL:-gemini-flash-latest}"

gcloud builds submit --tag "gcr.io/${PROJECT_ID}/${SERVICE}"

gcloud run deploy "${SERVICE}" \
  --image "gcr.io/${PROJECT_ID}/${SERVICE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars MODEL="${MODEL}"
