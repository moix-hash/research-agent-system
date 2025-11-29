# Research Agent System 

A multi-agent AI system for automated research and content creation, built for the Google AI Agents Intensive Course Capstone Project.

##  Overview

This system demonstrates a complete multi-agent architecture where specialized AI agents collaborate to automate research, content generation, and quality analysis. The system coordinates Research, Writing, Analysis, and Coordinator agents to transform research topics into comprehensive content packages.

##  Architecture
User Request → Coordinator Agent → Research Agent → Writing Agent → Analysis Agent → Final Result

### Agent Responsibilities:
- **Research Agent**: Conducts comprehensive topic research using web search and AI analysis
- **Writing Agent**: Generates professional content (articles, reports, blogs) based on research
- **Analysis Agent**: Evaluates content quality, sentiment, and readability
- **Coordinator Agent**: Manages workflow and communication between all agents

##  Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Development
```bash
# Clone repository
git clone https://github.com/moix-hash/research-agent-system.git 
cd research-agent-system

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your Gemini API key

# Start the server
python src/main.py

# Access the API documentation
# http://localhost:8000/docs
```
### Docker Deployment
```bash

# Build and run with Docker
docker build -t research-agent-system .
docker run -p 8000:8000 research-agent-system

# Or use Docker Compose for full stack
docker-compose up --build
```
##  API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | System information and available endpoints |
| `/research` | POST | Create new research task |
| `/tasks/{id}` | GET | Get specific task status and results |
| `/tasks` | GET | List all tasks |
| `/status` | GET | System status and metrics |
| `/health` | GET | Health check for all components |
| `/metrics` | GET | Prometheus metrics |
| `/docs` | GET | Interactive API documentation |
### Example Usage

**Windows PowerShell:**
```bash
# Create research task
Invoke-RestMethod -Uri "http://localhost:8000/research" -Method Post -ContentType "application/json" -Body '{"topic": "Artificial Intelligence in Healthcare", "content_type": "article", "tone": "professional"}'

# Check task status (replace with actual task_id)
Invoke-RestMethod -Uri "http://localhost:8000/tasks/YOUR_TASK_ID" -Method Get

# List all tasks
Invoke-RestMethod -Uri "http://localhost:8000/tasks" -Method Get

# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```
##  Features
Core Capabilities

    Automated Research: AI-powered topic research and analysis

    Content Generation: Professional writing in various formats and tones

    Quality Assessment: Automated content evaluation and improvement suggestions

    Multi-format Support: Articles, reports, blog posts, and more

### Technical Features

    RESTful API: Comprehensive API with OpenAPI documentation

    Real-time Processing: Background task processing with status tracking

    Error Handling: Graceful fallbacks when external services are unavailable

    Observability: Structured logging, metrics, and distributed tracing

    Containerization: Docker support for production deployment

##  Testing
```bash

# Run comprehensive API tests
python test_api.py

# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Quick validation
python quick_test.py
```
