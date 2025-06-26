from typing import List, Union
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import MCPServerAdapter
from typing import List
import os


@CrewBase
class CrewaiContext7Mcp():
    """CrewaiContext7Mcp crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    mcp_server_params: Union[list[MCPServerAdapter | dict[str, str]], MCPServerAdapter, dict[str, str]]  = {
        "url": f"https://server.smithery.ai/@upstash/context7-mcp/mcp?api_key={os.getenv('SMITHERY_API_KEY')}",
        "transport": "streamable-http",
    }

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            tools=self.get_mcp_tools() # GET
        )
    
    @agent
    def answer_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['answer_generator'], # type: ignore[index]
            verbose=True,
            tools=self.get_mcp_tools("get-library-docs") 
        )


    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiContext7Mcp crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
