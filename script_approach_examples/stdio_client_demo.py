from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os

# Create a StdioServerParameters object
server_params=StdioServerParameters(
    command="python3", 
    args=["servers/math_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ},
)

# Use the StdioServerParameters object to create a MCPServerAdapter
with MCPServerAdapter(server_params) as tools:
    print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")

    agent = Agent(
        role="Mathematician",
        goal="Perform mathematical operations.",
        backstory="An experienced mathematician that can perform mathematical operations via MCP tools.",
        tools=tools,
        verbose=True,
    )
    task = Task(
        description="Solve the math {problem} given to you by the user.",
        expected_output="The correct answer to the math problem using the available tools.",
        agent=agent,
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff(inputs={"problem": "power(2.25, 2)"})
    print(result)