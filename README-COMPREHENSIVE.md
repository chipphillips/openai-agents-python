# OpenAI Agents SDK: Comprehensive Guide

## Overview

The OpenAI Agents SDK is a powerful framework for building sophisticated AI applications using a multi-agent architecture. It provides a lightweight, flexible system for orchestrating one or more AI agents to work together on complex tasks. This SDK is the production-ready successor to OpenAI's earlier experimental framework called Swarm.

## Core Concepts

### Agents

An agent is the fundamental building block in the SDK. Each agent consists of:

- **Instructions**: Custom prompts (system messages) that define the agent's behavior
- **Tools**: Functions or capabilities the agent can access
- **Model**: Which LLM powers the agent (o3-mini, gpt-4o, etc.)
- **Handoffs**: Other agents that this agent can delegate to
- **Guardrails**: Input/output validation to ensure safety and quality

```python
from agents import Agent

agent = Agent(
    name="Construction Planner",
    instructions="You are a construction planning specialist. Help with project timelines, resource allocation, and scheduling.",
    model="gpt-4o",
)
```

### Handoffs

Handoffs allow agents to delegate tasks to other specialized agents. This is useful when you have agents with specific domains of expertise.

```python
from agents import Agent, handoff

materials_agent = Agent(
    name="Materials Specialist",
    instructions="You provide expert advice on construction materials, costs, and properties."
)

planning_agent = Agent(
    name="Planning Specialist",
    instructions="You help with project planning, timelines, and resource allocation.",
    handoffs=[handoff(materials_agent)]
)
```

### Tools

Tools let agents interact with external systems and data sources. The SDK supports:

1. **Function Tools**: Any Python function can be turned into a tool
2. **Hosted Tools**: Predefined tools like WebSearchTool, FileSearchTool, and ComputerTool
3. **Agents as Tools**: Using other agents as tools rather than via handoffs

```python
from agents import Agent, function_tool, WebSearchTool

@function_tool
def calculate_materials(square_footage: float, building_type: str) -> dict:
    """Calculate required construction materials based on square footage and building type."""
    # Calculation logic here
    return {"concrete": 12.5, "steel": 5.2, "lumber": 35.0}

agent = Agent(
    name="Construction Assistant",
    instructions="Help construction professionals plan projects.",
    tools=[
        calculate_materials, 
        WebSearchTool(user_location={"type": "approximate", "city": "New York"})
    ]
)
```

### Guardrails

Guardrails validate inputs and outputs for safety and quality. They run in parallel with agents and can quickly halt execution if needed.

```python
from agents import Agent, GuardrailFunctionOutput, input_guardrail, RunContextWrapper

@input_guardrail
async def construction_domain_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str
) -> GuardrailFunctionOutput:
    # Check if query is construction-related
    is_relevant = "construction" in input.lower() or "building" in input.lower()
    
    return GuardrailFunctionOutput(
        output_info={"is_relevant": is_relevant},
        tripwire_triggered=not is_relevant  # Stop if not construction-related
    )

agent = Agent(
    name="Construction Helper",
    instructions="You provide construction advice only.",
    input_guardrails=[construction_domain_guardrail]
)
```

### Tracing

The SDK includes built-in tracing capabilities for debugging, monitoring, and visualizing agent workflows. Each agent run generates a trace that captures:

- LLM calls and responses
- Tool invocations and results
- Handoffs between agents
- Guardrail evaluations
- Custom events

```python
from agents import Agent, Runner, trace

with trace(workflow_name="Construction Planning Process", group_id="project-123"):
    result = await Runner.run(agent, "What materials do I need for a 2000 sq ft commercial building?")
```

## Running Agents

The `Runner` class provides methods to execute agents:

```python
from agents import Agent, Runner

# Asynchronous execution
result = await Runner.run(agent, "Help me plan my construction project")

# Synchronous execution
result = Runner.run_sync(agent, "Help me plan my construction project")

# Streaming execution (for real-time updates)
streaming_result = await Runner.run_streamed(agent, "Help me plan my construction project")
async for event in streaming_result.stream_events():
    # Process streaming events
    pass
```

## Agent Patterns

The SDK supports several powerful design patterns:

1. **Deterministic Flows**: Breaking complex tasks into sequential steps
2. **Routing/Handoffs**: Directing queries to specialized agents
3. **Agents as Tools**: Using agents as callable functions
4. **LLM-as-a-Judge**: Using a second LLM to evaluate and improve outputs
5. **Parallelization**: Running multiple agents simultaneously
6. **Guardrails**: Validating inputs/outputs for safety and relevance

## Installation and Requirements

```bash
# Requires Python 3.9 or higher
pip install openai-agents
```

Environment variables:
```
OPENAI_API_KEY=your_api_key
```

## Example: Multi-Agent Construction Assistant

```python
import asyncio
from agents import Agent, Runner, WebSearchTool, function_tool, handoff, trace

# Define specialized agents
materials_agent = Agent(
    name="Materials Specialist",
    instructions="You are an expert on construction materials, costs, and properties. Provide specific, practical recommendations."
)

planning_agent = Agent(
    name="Planning Specialist",
    instructions="You help with construction project planning, timelines, and resource allocation."
)

safety_agent = Agent(
    name="Safety Specialist",
    instructions="You provide guidance on construction safety protocols, equipment, and regulations."
)

# Define tools
@function_tool
def estimate_cost(square_footage: float, building_type: str, location: str) -> str:
    """Estimate construction costs based on square footage, building type, and location."""
    # Simplified calculation for example
    base_costs = {
        "residential": 150,
        "commercial": 250,
        "industrial": 200
    }
    
    location_factors = {
        "urban": 1.5,
        "suburban": 1.2,
        "rural": 1.0
    }
    
    building_type = building_type.lower()
    location_type = location.lower()
    
    if building_type not in base_costs:
        return f"Unknown building type: {building_type}"
    
    if location_type not in location_factors:
        return f"Unknown location type: {location_type}"
    
    base_cost = base_costs[building_type]
    factor = location_factors[location_type]
    total = square_footage * base_cost * factor
    
    return f"Estimated cost for a {square_footage} sq ft {building_type} building in a {location_type} area: ${total:,.2f}"

# Create main triage agent
triage_agent = Agent(
    name="Construction Assistant",
    instructions="""
    You are a helpful assistant for construction professionals.
    
    - For questions about materials, handoff to the Materials Specialist
    - For questions about project planning, handoff to the Planning Specialist
    - For questions about safety, handoff to the Safety Specialist
    - For general questions or cost estimates, answer directly
    """,
    tools=[estimate_cost, WebSearchTool()],
    handoffs=[
        handoff(materials_agent),
        handoff(planning_agent),
        handoff(safety_agent)
    ]
)

async def main():
    with trace(workflow_name="Construction Assistant"):
        result = await Runner.run(
            triage_agent, 
            "I'm building a 5000 sq ft commercial building in an urban area. What will it cost and what materials should I consider for the exterior?"
        )
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [GitHub Repository](https://github.com/openai/openai-agents-python)
- [Examples Directory](examples/) - Contains numerous implementation examples

## License

This project is licensed under the MIT License. 