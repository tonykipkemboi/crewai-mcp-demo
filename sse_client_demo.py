from crewai import Agent, Task, Crew
from crewai_tools.adapters.mcp_adapter import MCPServerAdapter

import warnings
from pydantic import PydanticDeprecatedSince20

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

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
        verbose=True
    )

    doc_task = Task(
        description="Find the answer to: {question} using the available MCP tools.",
        agent=doc_agent,
        expected_output="""A very detailed and accurate answer to the user's Cloudflare question.
        IMPORTANT: Answer must be in the correct markdown format without any additional text or 
        the '```md' code block or '```'tags.
        """,
        output_file="output/doc_answer.md",
    )

    crew = Crew(
        agents=[doc_agent],
        tasks=[doc_task],
        verbose=True,
    )

    result = crew.kickoff(inputs={"question": input("Cloudflare docs, how may I help you? ") })
    print("\nFinal Output:\n", result)