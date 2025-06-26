from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Union
from mcp import StdioServerParameters
import os

@CrewBase
class MathematicianProject():
    """MathematicianProject crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    mcp_server_params: Union[list[StdioServerParameters | dict[str, str]], StdioServerParameters, dict[str, str]] = [
        StdioServerParameters(
            command="python3",
            args=["../servers/math_stdio_server.py"],
            env={"UV_PYTHON": "3.12", **os.environ},
        )
    ]

    @agent
    def mathematician(self) -> Agent:
        return Agent(
            config=self.agents_config['mathematician'], # type: ignore[index]
            verbose=True,
            tools=self.get_mcp_tools()
        )

    @task
    def math_task(self) -> Task:
        return Task(
            config=self.tasks_config['math_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MathematicianProject crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )