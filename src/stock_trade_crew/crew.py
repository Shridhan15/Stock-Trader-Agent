from typing import List
from crewai import Crew, Process, Task, Agent
from crewai.project import CrewBase, agent, task,crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
 

load_dotenv()
web_search_tool = SerperDevTool() 

@CrewBase  # ✅ No () after class name
class StockTradeCrew():  # ✅ Fixed syntax
    agents: List[BaseAgent]
    tasks: List[Task]
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Agents
    @agent
    def stock_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_market_analyst"],
            tools=[web_search_tool],  # ✅ Stock tool for analyst
        )

    @agent
    def stock_trader(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_trader"],
        )

    # Tasks  
    @task
    def stock_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["stock_analysis_task"],
        )

    @task
    def trade_decision_task(self) -> Task:
        return Task(
            config=self.tasks_config["trade_decision_task"],
            context=[self.stock_analysis_task()],  # ✅ Passes analyst output
            output_file="reports/report.md",
        )
 
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
