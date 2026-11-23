# k8s-pod-analyzer

A small Python tool that analyzes Kubernetes pod status and generates a health report.

## Features

- Parses `kubectl get pods` output (text or JSON format)
- Counts pods by status and by namespace
- Detects failing pods (not Running)
- Detects unstable pods (more than 5 restarts)
- Handles missing files and edge cases (empty cluster, missing container statuses)

Requires Python 3.10+

## Usage

```bash
kubectl get pods -A -o json > pods.json
python analyse.py
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

## Roadmap

- [ ] Read the file path from command-line arguments
- [ ] Fetch pod data directly from the Kubernetes API
- [ ] Add an AI-generated diagnosis for failing pods
