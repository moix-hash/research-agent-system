# Research Agent System

A comprehensive multi-agent AI system for automated research and content creation, built for the Google AI Agents Intensive Course Capstone Project.

##  Features

- **Multi-Agent Architecture**: Research, Writing, Analysis, and Coordinator agents working together
- **Automated Research**: Comprehensive topic research with web search integration
- **Content Generation**: AI-powered content creation in various formats and tones
- **Quality Analysis**: Automated content analysis and quality assessment
- **Memory Management**: Redis-backed memory bank for persistent context
- **Session Management**: Stateful session handling for complex tasks
- **Full Observability**: Logging, tracing, and metrics with OpenTelemetry
- **RESTful API**: Complete API with interactive documentation
- **Docker Support**: Containerized deployment with full stack

##  Architecture
Research Agent System/
├──  Agents/
│ ├── Research Agent - Conducts topic research
│ ├── Writing Agent - Generates content
│ ├── Analysis Agent - Analyzes content quality
│ └── Coordinator Agent - Manages workflow
├──  Tools/
│ ├── Web Search - Information gathering
│ ├── Code Execution - Python code validation
│ ├── File Operations - Data persistence
│ └── Custom Tools - Analysis and optimization
├──  Memory/
│ ├── Memory Bank - Long-term storage
│ └── Session Manager - State management
├──  Observability/
│ ├── Structured Logging
│ ├── Distributed Tracing
│ └── Metrics Collection
└──  API/
└── RESTful endpoints with full documentation

##  Installation

### Prerequisites

- Python 3.11+
- Redis (optional, for production)

### Quick Start

1. **Clone and setup**:
```bash
git clone <repository>

cd research_agent_system
