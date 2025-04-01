# AI Research Assistant

A modular, agentic AI system that automates research tasks by coordinating multiple specialized analyst personas. Built using LangGraph, this system conducts interviews, searches for relevant information, and produces cohesive research reports on any topic.

## Features

- **Multi-agent coordination**: Creates several analyst personas that tackle different aspects of a research topic
- **Automated research**: Conducts interviews with "experts", performs Google and Wikipedia searches
- **Human feedback loop**: Allows for human refinement of research analysts and topics
- **Report generation**: Automatically produces structured reports with proper citations

## System Architecture

The system is organized into several key components:

- **Models**: Data structures for analysts and state management
- **Configs**: LLM configurations, rate limiters, and system prompts
- **Nodes**: Function implementations for different graph nodes
- **Graphs**: Graph definitions that coordinate the workflow

## Installation

1. Clone the repository:
   ```
   git clone [repository-url]
   cd research_assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

## Usage

Run the research assistant with:

```
python main.py
```

The system will:
1. Create analyst personas based on the specified topic
2. Allow for human feedback to refine the analysts
3. Conduct interviews and research
4. Generate a complete report with introduction, insights, and conclusion

## Configuration

Adjust the main parameters in `main.py`:

```python
# Initialize parameters
max_analysts = 2  # Number of analyst personas to create
topic = "The impact of AI on the future of work"  # Research topic
```

## Project Structure

```
research_assistant/
├── main.py                  # Entry point
├── models/                  # Data models
│   ├── analyst.py           # Analyst and Analysts models
│   └── states.py            # State definitions
├── configs/                 # Configuration
│   └── settings.py          # LLM config and prompts
├── nodes/                   # Node implementations
│   ├── assistant_nodes.py   # Main assistant functions
│   └── interview_nodes.py   # Interview functions
├── graphs/                  # Graph definitions
│   ├── assistant_graph.py   # Main assistant graph
│   └── interview_graph.py   # Interview graph
└── utils/                   # Utility functions
```

## Example Output

The system produces a complete research report with:

1. An engaging title and introduction
2. Multiple sections covering different aspects of the topic
3. Proper citations of sources
4. A well-structured conclusion

## Extending the System

To add new capabilities:
- Add new node functions in the appropriate `nodes/` files
- Update graph definitions in `graphs/` to incorporate new nodes
- Add new state fields in `models/states.py` if needed

## Requirements

- Python 3.9+
- LangGraph
- LangChain
- Groq API key
- Google Serper API key 