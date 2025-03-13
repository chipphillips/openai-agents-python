# OpenAI Agents Examples for Construction Industry

This repository contains examples of using OpenAI's AI models to create agent-based systems for the construction industry. These examples demonstrate how to build AI assistants that can understand and address construction-specific queries.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- An OpenAI API key

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/openai-construction-agents.git
cd openai-construction-agents
```

2. Install the required dependencies:
```bash
pip install requests python-dotenv
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Examples

### 1. Simple Agent (`simple_agent.py`)

This example demonstrates a basic agent architecture that uses domain specialization to route construction queries to the appropriate expert agent:

- Planning Specialist
- Materials Specialist
- Safety Specialist

To run this example:
```bash
python simple_agent.py
```

### 2. Multi-Agent System (`multi_agent.py`)

This example demonstrates a more advanced multi-agent system with explicit handoffs between agents, conversation memory, and specialized construction knowledge domains.

To run this example:
```bash
python multi_agent.py
```

### 3. Hello Agent (`hello_agent.py`)

This is a simple "hello world" example that demonstrates the basic usage of OpenAI's API for a construction-focused assistant.

To run this example:
```bash
python hello_agent.py
```

## Features

- Domain-specific expertise in construction planning, materials, and safety
- Agent-to-agent handoffs for specialized knowledge
- Conversation context maintenance
- Construction industry-focused instruction sets

## Usage Tips

- For best results, be specific in your construction-related queries
- The agents maintain conversation history, so you can refer to previous questions
- Type 'exit' to quit any of the example applications
- In the multi-agent system, type 'reset' to start a new conversation

## Advanced Implementation Notes

These examples implement patterns similar to those in OpenAI's Agents SDK but using the direct OpenAI API. They demonstrate:

1. Agent specialization (different domains of expertise)
2. Agent orchestration (routing queries to the right specialist)
3. Agent handoffs (transferring control between agents)
4. System message customization (construction-specific instructions)

For production use, consider exploring OpenAI's official Agents SDK for more advanced features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
