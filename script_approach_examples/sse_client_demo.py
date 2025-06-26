from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

# Create a SSEServerParameters object
server_params = {"url": "https://docs.mcp.cloudflare.com/sse"}

# Use the SSEServerParameters object to create a MCPServerAdapter
with MCPServerAdapter(server_params) as tools:
    print("Available MCP Tools:", [tool.name for tool in tools])

    doc_agent = Agent(
        role="Cloudflare Doc Searcher",
        goal="Find answers to questions about Cloudflare products using the available MCP tool.",
        backstory="A helpful assistant for Cloudflare documentation.",
        tools=tools,
        reasoning=True,
        reasoning_steps=2,
        memory=True,
        verbose=True
    )

    doc_task = Task(
        description="Find the answer to: {question} using the available MCP tools.",
        expected_output="A very detailed and accurate answer to the user's Cloudflare question.",
        output_file="output/doc_answer.md",
        agent=doc_agent,
        markdown=True
    )

    crew = Crew(
        agents=[doc_agent],
        tasks=[doc_task],
        verbose=True,
    )

    result = crew.kickoff(inputs={"question": input("Cloudflare docs, how may I help you? ") })
    print("\nFinal Output:\n", result)