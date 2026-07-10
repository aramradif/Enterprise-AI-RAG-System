![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688?logo=fastapi)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)
![License](https://img.shields.io/badge/License-MIT-green)

# Enterprise AI RAG System

A production-oriented **Retrieval-Augmented Generation (RAG)** platform built with **FastAPI**, **OpenAI GPT-4o-mini**, **OpenAI Embeddings**, and **ChromaDB**.

The project demonstrates how modern enterprise AI systems combine **hybrid retrieval**, **vector search**, **conversation memory**, **streaming responses**, and **evaluation metrics** to deliver grounded, context-aware answers from custom knowledge bases.

Unlike a simple chatbot, this project is being developed as a complete **Enterprise AI Platform**, with an extensible architecture that will continue to evolve through observability, authentication, CI/CD, cloud deployment, and agentic AI capabilities.

![Enterprise Web Platform](assets/web-platform.png)

---

# Quick Start

1. Clone the repository
2. Install dependencies
3. Configure your `.env`
4. Start the FastAPI backend
5. Launch the Enterprise Web Platform

---

# Table of Contents

- Overview
- System Architecture
- Enterprise Web Platform
- Key Features
- Technology Stack
- Project Structure
- Installation
- Running the Backend API
- API Endpoints
- Roadmap

---

# Overview

Traditional Large Language Models generate responses using only the knowledge contained in their training data.

Retrieval-Augmented Generation (RAG) improves answer quality by retrieving relevant information from external documents before generating a response.

This project allows users to:

- Ingest enterprise documents
- Generate embeddings
- Store vectors in ChromaDB
- Perform hybrid retrieval
- Maintain conversation memory
- Stream AI responses
- Evaluate retrieval and generation performance
- Generate grounded answers using GPT-4o-mini

---

# System Architecture

![Architecture](assets/architecture.png)

```
                Documents
        (TXT • PDF • DOCX • MD)
                     │
                     ▼
          Enterprise Folder Loader
                     │
                     ▼
              Text Extraction
                     │
                     ▼
             Automatic Chunking
                     │
                     ▼
           OpenAI Embeddings
                     │
                     ▼
              ChromaDB Vector Store
                     │
                     ▼
      Hybrid Retrieval (Semantic + Keyword)
                     │
                     ▼
             Context Management
                     │
                     ▼
              Prompt Engineering
                     │
                     ▼
                GPT-4o-mini
                     │
                     ▼
            Grounded AI Response
```

---

# Enterprise Web Platform

The project includes an enterprise-style web platform that communicates directly with the FastAPI backend.

Current capabilities include:

- Streaming AI Chat
- Enterprise Evaluation Dashboard
- Persistent Chat State
- Hybrid Retrieval
- Conversation Memory
- Real-Time Evaluation Metrics
- Token Usage Tracking
- Estimated Cost Reporting
- Sidebar Navigation

The platform is designed to evolve into a complete Enterprise AI workspace featuring observability, authentication, administrative tooling, and cloud deployment.

![Enterprise Web Platform](assets/web-platform.png)

---

# Project Status

**Current Version:** v1.8

## Latest Release (v1.8)

### New Features

- Enterprise Logs Dashboard
- Persistent Request Logging
- Enterprise Observability API (`GET /logs`)
- Summary Metrics Dashboard
- Token Usage Tracking
- Cost Estimation
- Refreshable Logs Dashboard
- Enterprise UI Enhancements

### Improvements

- Improved dashboard layout
- Professional status badges
- Better timestamp formatting
- Cleaner metrics presentation
- Enhanced observability architecture

---

# Key Features

## AI & Retrieval

- Retrieval-Augmented Generation (RAG)
- GPT-4o-mini Integration
- OpenAI Embeddings
- Hybrid Retrieval (Semantic + Keyword)
- Intelligent Context Management
- Prompt Engineering
- Grounded AI Responses

---

## Knowledge Base

- ChromaDB Vector Database
- Enterprise Folder Loader
- Multi-format Document Ingestion
- Automatic Chunking
- Source Metadata & Citations

Supported document types:

- PDF
- DOCX
- TXT
- Markdown

---

## Conversation Intelligence

- Session-Based Memory
- Enterprise Conversation Memory
- Conversation Summaries
- Multi-turn Conversations
- Streaming Responses

---

## Enterprise Web Platform

- Enterprise Dashboard
- Interactive Streaming Chat
- Evaluation Dashboard
- Persistent Chat State
- Sidebar Navigation

---

## AI Evaluation

- Retrieval Latency
- LLM Latency
- Token Usage
- Prompt Tokens
- Completion Tokens
- Total Tokens
- Estimated Cost Tracking
- Documents Retrieved

---

## Backend

- FastAPI REST API
- Modular Enterprise Architecture
- Configurable Environment Variables
- End-to-End Enterprise AI Pipeline

---

# Technology Stack

## Backend

- Python 3.14
- FastAPI
- Uvicorn

## Artificial Intelligence

- OpenAI GPT-4o-mini
- text-embedding-3-small
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering

## Vector Database

- ChromaDB

## Document Processing

- PDF (pypdf)
- DOCX (python-docx)
- TXT
- Markdown

## Frontend

- HTML
- CSS
- JavaScript (ES Modules)

## Development

- Git
- GitHub
- VS Code

---

# Project Structure

```text
Enterprise-AI-RAG-System/
│
├── app/
│   ├── api/
│   ├── config/
│   ├── core/
│   ├── embeddings/
│   ├── evaluation/
│   ├── ingestion/
│   ├── llm/
│   ├── memory/
│   ├── models/
│   ├── retrieval/
│   └── services/
│
├── assets/
├── data/
├── frontend/
│   ├── js/
│   └── pages/
│
├── scripts/
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/aramradif/Enterprise-AI-RAG-System.git
```

Navigate into the project:

```bash
cd Enterprise-AI-RAG-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Backend API

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

![Swagger UI](assets/swagger-ui.png)

---

# API Endpoints

| Endpoint | Description |
|-----------|-------------|
| POST /ask | Standard RAG question answering |
| POST /ask/stream | Streaming AI responses |
| POST /evaluate | AI evaluation metrics |
| GET /health | Health check |

---

# Enterprise Web Platform

Launch the frontend using VS Code Live Server.

Open:

```
http://127.0.0.1:5500/frontend/index.html
```

The frontend currently supports:

- Streaming Chat
- Conversation Memory
- Enterprise Evaluation Dashboard
- Real-Time AI Metrics
- Persistent Chat State

---

# Roadmap

## ✅ Phase 1 — Enterprise Retrieval

- FastAPI Backend
- ChromaDB Integration
- Hybrid Retrieval
- Multi-format Document Support
- Prompt Engineering

## ✅ Phase 2 — GPT Integration

- GPT-4o-mini
- End-to-End Enterprise RAG Pipeline

## ✅ Phase 3 — Conversation Intelligence

- Session Memory
- Conversation Memory
- Conversation Summaries

## ✅ Phase 4 — Enterprise Web Platform

- Streaming Chat
- Sidebar Navigation
- Persistent Chat State

## ✅ Phase 5 — Enterprise AI Evaluation

- Evaluation Dashboard
- Retrieval Metrics
- Token Usage
- Cost Estimation

## 🔄 Phase 6 — Enterprise Observability

- Structured Logging
- Log Dashboard
- Request History

## ⏳ Phase 7 — Security

- Authentication
- Authorization
- User Management

## ⏳ Phase 8 — DevOps

- Docker
- Docker Compose
- CI/CD Pipeline
- Automated Testing

## ⏳ Phase 9 — Cloud Deployment

- AWS
- Azure
- Production Infrastructure

## ⏳ Phase 10 — Agentic AI

- Tool Calling
- Multi-Agent Workflows
- MCP Integration
- AI Automation

---

# License

This project is licensed under the MIT License.