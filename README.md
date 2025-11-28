---
title: Agentic Autonomous Quiz Solver
emoji: 🚀
colorFrom: red
colorTo: blue
sdk: docker
pinned: false
app_file: main.py
app_port: 7860
---

# Agentic Autonomous Quiz Solver

[![License:MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.3+-green.svg)](https://fastapi.tiangolo.com/)

---
A self-directed AI agent powered by **LangGraph** and **LangChain**, designed to tackle data-centric quizzes through *web scraping, data processing, analytical reasoning, and visualization*. The system leverages Google’s ***Gemini 2.5 Flash*** model to coordinate tool usage and guide decision-making.



## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Tools & Capabilities](#tools--capabilities)
- [Docker Deployment](#docker-deployment)
- [How It Works](#how-it-works)
- [License](#license)

## Overview

This project implements an **autonomous agent** capable of solving complex data-driven queries. Unlike traditional QA systems, it can actively browse the web, run Python code to analyze data, and iteratively refine its answers. It is designed to pass the Tools in Data Science (TDS) Project 2 evaluation criteria by seamlessly handling diverse tasks ranging from CSV analysis to image interpretation.

## Architecture

The agent is built on the **ReAct (Reasoning + Acting)** paradigm using:
- **LangGraph**: Manages the stateful workflow between the agent's reasoning (LLM) and execution (Tools) steps.
- **LangChain**: Provides the abstraction layer for LLM interaction and tool definitions.
- **FastAPI**: Exposes the agent logic as a production-ready REST API.

```
┌─────────────┐
│   FastAPI   │  ← Receives POST requests with quiz URLs
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Agent     │  ← LangGraph orchestrator with Gemini 2.5 Flash
│   (LLM)     │
└──────┬──────┘
       │
       ├────────────┬────────────┬─────────────┬──────────────┐
       ▼            ▼            ▼             ▼              ▼
   [Scraper]   [Downloader]  [Code Exec]  [POST Req]  [Add Deps]
```

### Key Components:

1. **FastAPI Server** (`main.py`): Handles incoming POST requests, validates secrets, and triggers the agent
2. **LangGraph Agent** (`agent.py`): State machine that coordinates tool usage and decision-making
3. **Tools Package** (`tools/`): Modular tools for different capabilities
4. **LLM**: Google Gemini 2.5 Flash with rate limiting (9 requests per minute)

## Features

- **🤖 Autonomous Reasoning**: Decomposes complex questions into step-by-step actions.
- **📊 Data Analytics**: Built-in Pandas support for filtering, sorting, and summarizing CSV data.
- **🕸️ Web Scraping**: Extracts live information from URLs to answer real-time queries.
- **🔍 Search**: Verifies facts and gathers context using external search engines.
- **🐳 Containerized**: Fully Dockerized for consistent deployment across environments.

## Project Structure

```bash
TDS-PROJECT-2/
├── app/
│ ├── agent.py # Core agent logic (LangGraph)
│ ├── tools.py # Tool definitions (Scraper, Analysis, etc.)
│ └── utils.py # Utility functions
├── data/ # Directory for input datasets
├── main.py # FastAPI application entry point
├── Dockerfile # Docker build configuration
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .env # Environment variables (API keys)
```

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/codemaster-vansh/TDS-PROJECT-2.git
cd TDS-PROJECT-2
```

### Step 2: Install Dependencies

#### Option A: Using `uv` (Recommended)


Ensure you have uv installed, then sync the project:

```bash
# Install uv if you haven't already  
pip install uv

# Sync dependencies  
uv sync
uv run playwright install chromium
```

Start the FastAPI server:
```bash
uv run main.py
```
The server will start at ```http://0.0.0.0:7860```.

#### Option B: Using `pip`

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium
```

## ⚙️Configuration

Create a `.env` file in the root directory to store your secrets.

```bash
#Required for the LLM
GEMINI_API_KEY=your_google_ai_studio_key

#Server Configuration
HOST=0.0.0.0
PORT=7860
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy it to your `.env` file

## 🚀 Usage

### Local Development

Start the FastAPI server:

```bash
# If using uv
uv run main.py

# If using standard Python
python main.py
```

The server will start on `http://0.0.0.0:7860`

### Testing the Endpoint

Send a POST request to test your setup:

```bash
curl -X POST http://localhost:7860/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your_secret_string",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

Expected response:

```json
{
  "status": "ok"
}
```

The agent will run in the background and solve the quiz chain autonomously.

## 🌐 API Endpoints

### `POST /solve`

Receives quiz tasks and triggers the autonomous agent.

**Request Body:**

```json
{
  "email": "your.email@example.com",
  "secret": "your_secret_string",
  "url": "https://example.com/quiz-123"
}
```

**Responses:**

| Status Code | Description                    |
| ----------- | ------------------------------ |
| `200`     | Secret verified, agent started |
| `400`     | Invalid JSON payload           |
| `403`     | Invalid secret                 |
| `405`     | Incorrect Request Made

### `GET /health`

Health check endpoint for monitoring.

**Response:**

```json
{
  "status": "ok",
  "uptime_seconds": 3600
}
```

## 🛠️ Tools & Capabilities

The agent has access to the following tools:

### 1. **Web Scraper** (`get_rendered_html`)

- Uses Playwright to render JavaScript-heavy pages
- Waits for network idle before extracting content
- Returns fully rendered HTML for parsing

### 2. **File Downloader** (`download_file`)

- Downloads files (PDFs, CSVs, images, etc.) from direct URLs
- Saves files to `AgentFiles/` directory
- Returns the saved filename

### 3. **Code Executor** (`run_code`)

- Executes arbitrary Python code in an isolated subprocess
- Returns stdout, stderr, and exit code
- Useful for data processing, analysis, and visualization

### 4. **POST Request** (`post_request`)

- Sends JSON payloads to submission endpoints
- Includes automatic error handling and response parsing
- Prevents resubmission if answer is incorrect and time limit exceeded

### 5. **Dependency Installer** (`add_dependencies`)

- Dynamically installs Python packages as needed
- Uses `uv add` for fast package resolution
- Enables the agent to adapt to different task requirements

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t TDS-PROJECT-2 .
```

### Run the Container

```bash
docker run -p 7860:7860 \
  -e EMAIL="your.email@example.com" \
  -e SECRET="your_secret_string" \
  -e GOOGLE_API_KEY="your_api_key" \
  llm-analysis-agent
```

### Deploy to HuggingFace Spaces

1. Create a new Space with Docker SDK
2. Push this repository to your Space
3. Add secrets in Space settings:
   - `EMAIL`
   - `SECRET`
   - `GOOGLE_API_KEY`
4. The Space will automatically build and deploy

## 📝 Key Design Decisions

1. **LangGraph over Sequential Execution**: Allows flexible routing and complex decision-making
2. **Background Processing**: Prevents HTTP timeouts for long-running quiz chains
3. **Tool Modularity**: Each tool is independent and can be tested/debugged separately
4. **Rate Limiting**: Prevents API quota exhaustion (9 req/min for Gemini)
5. **Code Execution**: Dynamically generates and runs Python for complex data tasks
6. **Playwright for Scraping**: Handles JavaScript-rendered pages that `requests` cannot
7. **`uv` for Dependencies**: Fast package resolution and installation

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author**: Vansh Whig  
**Course**: Tools in Data Science (TDS)  
**Institution**: IIT Madras

For questions or issues, please open an issue on the [GitHub repository](https://github.com/codemaster-vansh/TDS-PROJECT-2) or contact me at this [email](mailto:vanshwhig24@gmail.com)