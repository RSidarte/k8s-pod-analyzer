# k8s-pod-analyzer

A small Python tool that analyzes Kubernetes pod status and generates a health report.

## Features

- Parses `kubectl get pods` output (text or JSON format)
- Counts pods by status and by namespace
- Detects failing pods (not Running)
- Detects unstable pods (more than 5 restarts)
- Handles missing files and edge cases (empty cluster, missing container statuses)
- AI-powered diagnosis of failing pods (Claude API)

## Installation

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
```

## Configuration

The AI diagnosis requires an Anthropic API key.

```bash
cp .env.example .env
```

Then edit `.env` and set `ANTHROPIC_API_KEY`. Never commit this file.

## Usage

```bash
kubectl get pods -A -o json > pods.json

python analyse.py   # health report
python llm.py       # AI diagnosis of failing pods
```

## Example output

```
=== Rapport du cluster ===
Total : 4 pods
=== Par statut ===
Running : 3
Pending : 1
=== Par namespace ===
prod : 2
batch : 2
Pods en erreur : worker-1
Pods instables (> 5 restarts) : api-2, worker-2
```

### AI diagnosis (`llm.py`), excerpt

> #### worker-1 (batch) : Pending, 0 restarts
>
> **Causes probables :**
> - Ressources insuffisantes sur les nœuds (`Insufficient cpu/memory`)
> - Taints/tolerations ou nodeSelector/affinity impossibles à satisfaire
> - PVC non bound (volume non provisionné ou StorageClass inexistante)
>
> **Commandes :** `kubectl -n batch describe pod worker-1`, `kubectl -n batch get pvc`…

## Roadmap

- [ ] Read the file path from command-line arguments
- [ ] Fetch pod data directly from the Kubernetes API
- [x] Add an AI-generated diagnosis for failing pods
