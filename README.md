<!-- PROJECT SHIELDS -->
<p align="center">
  <a href="https://github.com/tanushdev/sc_api"><img src="https://img.shields.io/github/license/tanushdev/sc_api?style=for-the-badge" alt="License"></a>
  <a href="https://img.shields.io/github/last-commit/tanushdev/sc_api"><img src="https://img.shields.io/github/last-commit/tanushdev/sc_api?style=for-the-badge" alt="Last Commit"></a>
  <a href="#"><img src="https://img.shields.io/badge/python-3.9%2B-blue?style=for-the-badge" alt="Python"></a>
  <a href="#"><img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge" alt="FastAPI"></a>
  <a href="#"><img src="https://img.shields.io/badge/Docs-OpenAPI-795EF0?style=for-the-badge" alt="OpenAPI"></a>
</p>

<h1 align="center">SC_API</h1>
<p align="center"><i>Empowering Seamless ESG Insights at Scale</i></p>

<p align="center">
  <img src="docs/overview.png" alt="SC_API Overview" width="600">
</p>

<p align="center">
  <a href="#quickstart"><b>Quickstart</b></a> •
  <a href="#features"><b>Features</b></a> •
  <a href="#api-reference"><b>API</b></a> •
  <a href="#deploy"><b>Deploy</b></a> •
  <a href="#contributing"><b>Contribute</b></a>
</p>

---

## ✨ Overview
**SC_API** is a developer-focused toolkit to extract and analyze **ESG** content from PDFs. It exposes clean REST endpoints for upload → parse → analyze workflows, with a UI for batch uploads and real‑time progress. Designed for security, provenance, and horizontal scalability.

### Why SC_API?
- **Semantic ESG Analysis** — classify & score environment/ESG/actions/claims from documents.
- **Production‑ready API** — simple, fast endpoints for ingestion and retrieval.
- **Security & Provenance** — automatic metadata + checksums for auditability.
- **Nice UI** — upload multiple PDFs, view statuses & results live.
- **Cloud‑native** — container‑first; deploy with Docker or Kubernetes.

---

## 🧭 Project Structure
```
sc_api/
├─ backend/
│  ├─ app/
│  │  ├─ main.py            # FastAPI app & routes
│  │  └─ services/          # parsing, NLP, scoring
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ public/               
│  ├─ src/                   # React / UI
│  └─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

> Tip: Adjust the tree to mirror your exact repo; this is the suggested layout used in examples below.

---

## 🚀 Quickstart
### Prerequisites
- Python **3.9+**
- Node.js **18+** (for the UI)
- Docker (optional but recommended)

### 1) Clone
```bash
git clone https://github.com/tanushdev/sc_api.git
cd sc_api
```

### 2) Backend (FastAPI)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Open **http://localhost:8000/docs** for interactive API docs.

### 3) Frontend (UI)
```bash
cd ../frontend
npm install
npm run dev
```
Open the printed local URL (e.g. **http://localhost:5173/**).

---

## 🧪 Example Usage (API)
### Upload & analyze a PDF
```bash
curl -X POST "http://localhost:8000/analyze"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"   -F "file=@sample.pdf"
```
**Response (example)**
```json
{
  "document_id": "doc_abc123",
  "status": "processed",
  "scores": {
    "environment": 0.82,
    "esg": 0.77,
    "actions": 0.61,
    "claims": 0.23,
    "net_action": 0.38
  },
  "provenance": {
    "sha256": "…",
    "received_at": "2025-09-04T04:31:32Z"
  }
}
```

### Get results
```bash
curl -X GET "http://localhost:8000/results/doc_abc123"
```

---

## 🧰 Features
- **PDF ingestion** with queueing & status tracking
- **NLP pipeline** (spaCy / transformers-ready) for ESG signal extraction
- **Scoring & aggregation** per document and per company
- **Provenance ledger** with hashes, timestamps, and source hints
- **Realtime UI** with upload progress + result previews
- **OpenAPI docs** at `/docs` and `/redoc`

---

## 🐳 Deploy
### Docker
```bash
docker compose up -d --build
```
- Backend: `http://localhost:8000`
- Frontend: printed by the container (e.g. `http://localhost:5173`)

### Environment
Create a `.env` (backend) with values like:
```
APP_ENV=dev
LOG_LEVEL=INFO
MAX_WORKERS=4
```

---

## 📚 API Reference
When running locally, see **/docs** for interactive Swagger UI.

**Key Endpoints**
- `POST /analyze` – Upload & analyze a PDF
- `GET  /results/{{document_id}}` – Retrieve analysis by id
- `GET  /health` – Service healthcheck

> Optional: add more endpoints (batch upload, provenance export, etc.).

---


