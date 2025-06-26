from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

# Create a StreamableHTTPServerParameters object
server_params = {
    "url": "http://localhost:8001/mcp", 
    "transport": "streamable-http"
}

# Use the StreamableHTTPServerParameters object to create a MCPServerAdapter
with MCPServerAdapter(server_params) as tools:
    print("Available MCP Tools:", [tool.name for tool in tools])

    doc_agent = Agent(
        role="Hello World",
        goal="Greet the user.",
        backstory="A helpful assistant for greeting users.",
        tools=tools,
        verbose=True
    )

    doc_task = Task(
        description="Greet the {user}.",
        agent=doc_agent,
        expected_output="A very friendly greeting to the {user}.",
        markdown=True
    )

    crew = Crew(
        agents=[doc_agent],
        tasks=[doc_task],
        verbose=True,
    )

    result = crew.kickoff(inputs={"user": input("I'll say hello to you if you say your name. What's your name? ") })
    print("\nFinal Output:\n", result)