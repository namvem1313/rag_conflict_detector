---

# Project Documentation – RAG Conflict Detector

## Overview

RAG Conflict Detector is a Retrieval-Augmented Generation system tailored for enterprise knowledge management where documentation evolves rapidly. It intelligently ingests documents, detects and flags semantic contradictions (e.g., formula changes), and supports conflict-aware question answering using LLMs.

---

## Key Components

### 1. **Ingestion Pipeline**

* Supports versioned document ingestion
* Stores sentence embeddings (FAISS) and raw text
* Flags new entries that contradict previous knowledge using NLI model

### 2. **Vector Store**

* Uses `faiss.IndexFlatL2` with 384-d embeddings from Sentence Transformers
* Metadata stored in `rag_data.db` alongside vectors

### 3. **Conflict Detection**

* NLI (e.g., RoBERTa-MNLI) determines semantic contradiction
* Detected conflicts are logged with both old and new claims

### 4. **Query Interface (RAG)**

* Takes a question, retrieves top-k relevant sentences
* Checks for contradiction among results
* Returns all relevant info + flags if inconsistency is found

### 5. **Review Dashboard**

* Built with Streamlit
* Displays unresolved conflicts
* Lets reviewer log human resolutions

---

## Models Used

| Purpose            | Model                                      |
| ------------------ | ------------------------------------------ |
| Embedding          | `all-MiniLM-L6-v2` (Sentence Transformers) |
| Conflict Detection | `roberta-large-mnli` (HuggingFace)         |
| QA Generation      | `distilbert-base-uncased-distilled-squad`  |

---

## Database Schema (SQLite – rag\_data.db)

### `embeddings`

| Column  | Type |
| ------- | ---- |
| doc\_id | TEXT |
| vector  | TEXT |
| version | TEXT |
| text    | TEXT |

### `conflicts`

| Column            | Type      |
| ----------------- | --------- |
| id (PK)           | INTEGER   |
| doc\_id           | TEXT      |
| previous\_version | TEXT      |
| new\_version      | TEXT      |
| resolution        | TEXT      |
| timestamp         | TIMESTAMP |

---

## Incremental Ingestion Support

* System handles ingestion of new versions for existing `doc_id`s
* Automatically checks for conflicts during ingestion

---

## Example Workflow

1. `/ingest` receives: `doc_id=Formula_A_v2`, `text="Formula A = x - y"`
2. Checks DB: if `Formula A = x + y` exists
3. Detects contradiction → logs in `conflicts` table
4. Reviewer UI presents for approval/resolution
5. `/ask` fetches both and flags conflicting answer

---

## Test Commands

```bash
python main.py  # Launch Flask app
curl -X POST http://localhost:5055/ingest -d '{"doc_id": ..., "text": ..., "version": ...}'
streamlit run review_ui.py  # Run dashboard
```

---

# Deployment Plan – Terraform & Cloud Setup

## Goal

Deploy the RAG Conflict Detector system on AWS using ECS (Fargate), with persistent storage via EFS and automated updates from a Docker image in ECR.

---

## Infrastructure Overview

| Component       | Description                             |
| --------------- | --------------------------------------- |
| ECS Cluster     | Manages service tasks                   |
| Fargate Service | Runs containerized app (main.py)        |
| ECR             | Hosts Docker image                      |
| EFS             | Mounts SQLite DB for persistence        |
| ALB             | Application Load Balancer for Flask API |
| Terraform       | IAC for provisioning all components     |

---

## Directory: `deploy/terraform/`

### Key Files:

* `main.tf`: AWS provider config + ECR + ECS
* `ecs.tf`: Task definition, IAM roles, networking
* `efs.tf`: Elastic File System setup
* `alb.tf`: Load Balancer + route to ECS
* `variables.tf`: Environment config vars

---

## Deploy Commands

```bash
cd deploy/terraform
terraform init
terraform apply
```

Update `image_uri` in task definition to point to your ECR image.

---

## Dockerfile Summary

* Installs all Python deps (from `requirements.txt`)
* Exposes port 5055 for Flask
* CMD runs `main.py`

---

## Cloud Integration Notes

* EFS allows multiple task restarts without losing DB state
* Logs are piped to CloudWatch (via ECS config)
* Secure with HTTPS via ACM + Route53 (optional)

---

## Next Steps

* Add API Gateway + Auth
* Add batch document ingestion via S3
* Replace SQLite with RDS or DynamoDB
* Scale QA with GPU inference (SageMaker or Bedrock)

---
