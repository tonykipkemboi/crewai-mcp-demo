from typing import Union
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from mcp import StdioServerParameters
from typing import List
from pathlib import Path

@CrewBase
class SnowflakeMcpDemo():
    """SnowflakeMcpDemo crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Semantic model file
    config_path = Path(__file__).parent / "snowflake_demo_config.yaml"

    # Snowflake credentials
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    username = os.getenv("SNOWFLAKE_USER")
    pat = os.getenv("SNOWFLAKE_PAT")

    # Configure Snowflake MCP server
    mcp_server_params: Union[list[StdioServerParameters | dict[str, str]], StdioServerParameters, dict[str, str]] = [
            StdioServerParameters(
            command="uvx",
            args=[
                "--from", 
                "git+https://github.com/Snowflake-Labs/mcp",
                "mcp-server-snowflake",
                "--service-config-file",
                str(config_path),
                "--account-identifier",
                account,
                "--username", 
                username,
                "--pat",
                pat
            ],
            env={**os.environ}
        )
    ]

    @agent
    def regulatory_intelligence_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['regulatory_intelligence_agent'], 
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def portfolio_sec_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['portfolio_sec_analyst'], 
            verbose=True,
            tools=self.get_mcp_tools()
        )

    @agent
    def market_news_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_news_analyst'], 
            verbose=True,
            tools=[SerperDevTool()]
        )

    @task
    def regulatory_intelligence_task(self) -> Task:
        return Task(
            config=self.tasks_config['regulatory_intelligence_task'], 
        )

    @task
    def portfolio_sec_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['portfolio_sec_analysis_task'],
            output_file="output/snowflake_data/portfolio_sec_analysis_task.md"
        )

    @task
    def market_news_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_news_analysis_task'], 
            output_file="output/market_news_analysis_task.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SnowflakeMcpDemo crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
