#!/bin/bash
set -uo pipefail  # Removed -e to continue on errors

# Ensure jq is present
if ! command -v jq >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y jq
fi

PROJECT="${GCP_PROJECT_ID}"
CHANGED_BOTS="${1:-}"
GITHUB_SHA="${GITHUB_SHA}"
SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
GITHUB_REPOSITORY="${GITHUB_REPOSITORY}"

if [[ -z "$CHANGED_BOTS" ]]; then
  echo "No bots provided to deploy"
  exit 0
fi

# Get all secrets from GCP
mapfile -t ALL_SECRETS < <(gcloud secrets list --project "$PROJECT" --format='value(name)' || true)

# Function to convert secret name to env var name
to_env_name() {
  local s="$1"
  s="${s^^}"
  s="$(echo "$s" | sed 's/[^A-Z0-9_]/_/g')"
  s="$(echo "$s" | sed 's/__*/_/g')"
  s="$(echo "$s" | sed 's/^_//; s/_$//')"
  [[ "$s" =~ ^[0-9] ]] && s="S_${s}"
  [[ -z "$s" ]] && s="SECRET"
  echo "$s"
}

# Build secret args for Cloud Run
declare -A USED_ENV_NAMES=()
SECRET_ARGS_COMMON=()
for SECRET_ID in "${ALL_SECRETS[@]}"; do
  if ! gcloud secrets versions list "$SECRET_ID" --project "$PROJECT" \
        --filter='state=ENABLED' --format='value(name)' --limit=1 | grep -q .; then
    continue
  fi
  ENV_NAME="$(to_env_name "$SECRET_ID")"
  BASE="$ENV_NAME"; i=2
  while [[ -n "${USED_ENV_NAMES[$ENV_NAME]:-}" ]]; do
    ENV_NAME="${BASE}_${i}"; ((i++))
  done
  USED_ENV_NAMES["$ENV_NAME"]=1
  SECRET_ARGS_COMMON+=( "--set-secrets" "${ENV_NAME}=${SECRET_ID}:latest" )
done

# Deploy each bot
while IFS= read -r BOT_NAME; do
  [[ -z "${BOT_NAME:-}" ]] && continue

  IMAGE="us-east1-docker.pkg.dev/${PROJECT}/bots-repo/$BOT_NAME:${GITHUB_SHA}"

  # Check existence BEFORE deploy
  if gcloud run services describe "$BOT_NAME" --region us-east1 >/dev/null 2>&1; then
    EXISTED_BEFORE="true"
  else
    EXISTED_BEFORE="false"
  fi
  echo "Service $BOT_NAME existed before: $EXISTED_BEFORE"

  gcloud run deploy "$BOT_NAME" \
    --image "$IMAGE" \
    --region us-east1 \
    --platform managed \
    --service-account "cr-bots-runtime@${PROJECT}.iam.gserviceaccount.com" \
    --allow-unauthenticated \
    --port 8080 \
    "${SECRET_ARGS_COMMON[@]}"

  URL="$(gcloud run services describe "$BOT_NAME" --region us-east1 --format='value(status.url)')"
  ACTION=$([ "$EXISTED_BEFORE" = "true" ] && echo "updated" || echo "created")

  # Send Slack notification if webhook configured
  if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
    payload="$(jq -n \
      --arg action "$ACTION" \
      --arg bot "$BOT_NAME" \
      --arg project "$PROJECT" \
      --arg image "$IMAGE" \
      --arg url "$URL" \
      --arg repo "$GITHUB_REPOSITORY" \
      --arg sha "$GITHUB_SHA" \
      '{
        text: ":rocket: Bot \($action)",
        blocks: [
          { "type": "section", "text": { "type": "mrkdwn", "text": (":rocket: *Bot " + $action + "*") } },
          { "type": "section", "fields": [
              { "type": "mrkdwn", "text": "*Bot:* `\($bot)`" },
              { "type": "mrkdwn", "text": "*Project:* `\($project)`" },
              { "type": "mrkdwn", "text": "*Image:* `\($image)`" },
              { "type": "mrkdwn", "text": "*Commit:* <https://github.com/\($repo)/commit/\($sha)|`\($sha[0:7])`>" }
          ]},
          { "type": "section", "text": { "type": "mrkdwn", "text": "*URL:* <\($url)|\($url)>" } }
        ]
      }')"

    # Follow redirects; capture headers and body
    HTTP_CODE=$(curl -sS -L -X POST \
      -H 'Content-type: application/json' \
      --data "$payload" \
      -D /tmp/slack_headers.txt \
      -o /tmp/slack_resp.txt \
      -w "%{http_code}" \
      "$SLACK_WEBHOOK_URL" || true)

    echo "Slack HTTP $HTTP_CODE"
    echo "Slack headers:"
    sed -n '1,200p' /tmp/slack_headers.txt
    echo "Slack response:"
    sed -n '1,200p' /tmp/slack_resp.txt

    if [[ "$HTTP_CODE" -lt 200 || "$HTTP_CODE" -ge 300 ]]; then
      echo "Slack webhook failed" >&2
      exit 1
    fi
  else
    echo "SLACK_WEBHOOK_URL not set; skipping Slack notification."
  fi

done <<< "$CHANGED_BOTS"