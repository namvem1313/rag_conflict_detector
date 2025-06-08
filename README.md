# RAG Conflict Detector

A Retrieval-Augmented Generation (RAG) system that intelligently ingests documents, detects conflicting claims (e.g., contradictory formulas), and uses large language models (LLMs) to answer user questions based on relevant context.

---

## Features

- **Vector DB** with FAISS for semantic search
- **LLM-powered conflict detection** using NLI
- **Retrieval-Augmented Generation (RAG)** for answering questions
- **Flask API** for ingesting docs and asking questions
- **Review Dashboard** built with Streamlit for human-in-the-loop resolution
- **Modular, testable code** with logging + sample scripts
- **Deployment-ready** with Docker + Terraform (AWS ECS)

---

## Installation

```bash
git clone https://github.com/namvem1313/rag-conflict-detector.git
cd rag-conflict-detector

python -m venv rag_env
source rag_env/bin/activate  # or .\rag_env\Scripts\activate on Windows

pip install -r requirements.txt
```

If using python3 -> use 

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

---

## Run the API

```bash
python main.py
```

API runs at `http://localhost:5000`

---

## API Endpoints

| Method | Endpoint       | Description                          |
|--------|----------------|--------------------------------------|
| POST   | `/ingest`      | Ingest a document                    |
| POST   | `/ask`         | Ask a question (RAG response)        |

### Example: Ingest

```json
POST /ingest
{
  "doc_id": "doc_2021",
  "text": "Formula A = x + y"
}
```

### Example: Ask

```json
POST /ask
{
  "question": "What is Formula A?"
}
```

---

## Run Tests

```bash
python -m unittest discover -s tests
```

---

## Project Structure

```
rag_conflict_system/
├── app/                # Vector store, models, ingestion, retrieval
├── api/                # Flask routes
├── scripts/            # Load example documents
├── tests/              # Unit tests
├── deploy/             # Dockerfile, Terraform
├── config/             # YAML configuration
├── main.py             # App entry point
└── requirements.txt
```

---

## Review Dashboard (Streamlit)

streamlit run review_ui.py

Features:
  View unresolved conflicts
  Update resolution text per conflict
  Filter resolved vs unresolved

---

## Docker Deployment

docker build -t rag-conflict-detector .
docker run -p 5050:5050 rag-conflict-detector

## AWS Terraform Deployment

cd deploy/terraform
terraform init
terraform apply

Update the variables in variables.tf and ensure:
  Your Docker image is pushed to ECR
  Valid AWS credentials are configured
  Subnets and security groups are mapped

For AWS ECS:
  ```bash
  cd deploy/terraform
  terraform init
  terraform apply
  ```

Update:
  - `ECR image`
  - `IAM roles`
  - `subnets`, `security groups`

---

## Roadmap

| Version | Features |
|---------|----------|
| MVP     | Local conflict detection and Resolution through Dashboard + QA via RAG + Streamlit conflict resolution dashboard |
| v1      | Docker + ECS deployment |
| v2      | Source traceability + UI enhancement |
| v3      | Active learning & automated resolution |

---

## License

MIT License.
Copyright (c) 2025 Lakshmi Namratha Vempaty

This project uses the following open-source libraries and models:

- `sentence-transformers (MiniLM)` – Apache 2.0
- `transformers` – Apache 2.0
- `roberta-large-mnli` – MIT
- `distilbert-base-uncased-distilled-squad` – Apache 2.0
- `FAISS` – MIT
- `Flask` – BSD-3
- `Streamlit` – Apache 2.0
