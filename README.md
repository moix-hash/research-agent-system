# Research Agent System 🤖

A multi-agent AI system for automated research and content creation, built for the Google AI Agents Intensive Course Capstone Project.

## 🎯 Overview

This system demonstrates a complete multi-agent architecture where specialized AI agents collaborate to automate research, content generation, and quality analysis. The system coordinates Research, Writing, Analysis, and Coordinator agents to transform research topics into comprehensive content packages.

## 🏗️ Architecture
User Request → Coordinator Agent → Research Agent → Writing Agent → Analysis Agent → Final Result

### Agent Responsibilities:
- **Research Agent**: Conducts comprehensive topic research using web search and AI analysis
- **Writing Agent**: Generates professional content (articles, reports, blogs) based on research
- **Analysis Agent**: Evaluates content quality, sentiment, and readability
- **Coordinator Agent**: Manages workflow and communication between all agents

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)

### Local Development
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/research-agent-system.git
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
