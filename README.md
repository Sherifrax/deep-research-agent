# Deep Research Agent

A multi-agent AI system for conducting deep research and generating comprehensive reports using OpenAI's API.

## Features

- **Multi-Agent Architecture**: Uses specialized agents for planning, searching, writing, and email communication
- **Research Manager**: Orchestrates the research workflow
- **Search Integration**: Real-time web search capabilities
- **Email Integration**: Can send research findings via email
- **Gradio UI**: Interactive web interface for easy access

## Architecture

- `research_manager.py` - Orchestrates the multi-agent workflow
- `planner_agent.py` - Breaks down research topics into actionable tasks
- `search_agent.py` - Conducts web searches and retrieves information
- `writer_agent.py` - Synthesizes findings into comprehensive reports
- `email_agent.py` - Handles email delivery of results
- `messenger.py` - Communication layer between agents
- `app.py` - Gradio interface
- `simple.py` - Simple example usage
- `styles.py` - UI styling

## Setup

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Web UI

```bash
python app.py
```

Visit `http://localhost:7860` in your browser.

### Programmatic Usage

```python
from research_manager import ResearchManager

manager = ResearchManager()
results = manager.conduct_research("Your research topic")
```

## Deployment

### Render

This application is configured for deployment on [Render](https://render.com):

1. Create a new Web Service on Render
2. Connect this GitHub repository
3. Set environment variables (OPENAI_API_KEY)
4. Render will automatically detect `app.py` and `requirements.txt`

**Build Command**: `pip install -r requirements.txt`
**Start Command**: `python app.py`

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
