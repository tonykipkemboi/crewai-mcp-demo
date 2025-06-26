from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

import os

server_configurations = [
    # Streamable HTTP Server
    {
        "url": "http://localhost:8001/mcp", 
        "transport": "streamable-http"
    },
    # SSE Server
    {
        "url": "https://docs.mcp.cloudflare.com/sse"
    },
    # StdIO Server
    StdioServerParameters(
        command="python3",
        args=["servers/math_stdio_server.py"],
        env={"UV_PYTHON": "3.12", **os.environ},
    )
]

with MCPServerAdapter(server_configurations) as tools:
    print("Available MCP Tools:", [tool.name for tool in tools])

    hello_agent = Agent(
        role="Hello World",
        goal="Greet the user.",
        backstory="A helpful assistant for greeting users.",
        tools=tools,
        reasoning=True,
        reasoning_steps=2,
        verbose=True
    )

    math_agent = Agent(
        role="Mathematician",
        goal="Perform mathematical operations.",
        backstory="An experienced mathematician that can perform mathematical operations via MCP tools.",
        tools=tools,
        reasoning=True,
        reasoning_steps=2,
        verbose=True
    )

    docs_agent = Agent(
        role="Cloudflare Doc Searcher",
        goal="Find answers to questions about Cloudflare products using the available MCP tool.",
        backstory="A helpful assistant for Cloudflare documentation.",
        tools=tools,
        reasoning=True,
        reasoning_steps=2,
        verbose=True
    )

    summary_agent = Agent(
        role="Summary Assistant",
        goal="Summarize the output of the other agents.",
        backstory="A helpful assistant for summarizing the output of other agents.",
        tools=tools,
        reasoning=True,
        reasoning_steps=2,
        verbose=True
    )

    hello_task = Task(
        description="Greet the {user}.",
        agent=hello_agent,
        expected_output="A friendly greeting to the {user}.",
        markdown=True
    )

    math_task = Task(
        description="Perform a mathematical operation using the available tools for this {problem}.",
        agent=math_agent,
        expected_output="The result of the mathematical operation.",
        markdown=True
    )

    docs_task = Task(
        description="Find the answer to: {question} using the available MCP tools.",
        expected_output="A very detailed and accurate answer to the user's Cloudflare question.",
        output_file="output/cloudflare_answer.md",
        agent=docs_agent,
        markdown=True
    )

    summary_task = Task(
        description="Summarize the output of the other agents.",
        agent=summary_agent,
        expected_output="""A summary of the output of the other agents in markdown format.
        Structure of the summary:
        - Hello Task: hello_task result
        - Math Task: math_task result
        - Docs Task: docs_task result
        Do not include any additional text other than the summary.
        """,
        markdown=True,
        context=[hello_task, math_task, docs_task],
        output_file="output/summary.md"
    )

    crew = Crew(
        agents=[hello_agent, math_agent, docs_agent, summary_agent],
        tasks=[hello_task, math_task, docs_task, summary_task],
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "user": input("I'll say hello to you if you say your name. What's your name? "), 
            "problem": input("What's the math problem? "),
            "question": input("Cloudflare docs, how may I help you? ") 
        })
    print("\nFinal Output:\n", result)