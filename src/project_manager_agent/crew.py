from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai import LLM


llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)


@CrewBase
class ProjectManagerCrew:
    """ProjectManagerCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def project_strategist(self) -> Agent:
        print("ok")
        return Agent(
            config=self.agents_config["project_strategist"],
            verbose=True,
            llm=llm,
        )

    @agent
    def team_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["team_architect"],
            verbose=True,
            llm=llm,
        )

    @agent
    def project_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["project_planner"],
            verbose=True,
            llm=llm,
        )

    @agent
    def pmo_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["pmo_reporter"],
            verbose=True,
            llm=llm,
        )

    @task
    def define_scope_and_objectives(self) -> Task:
        return Task(
            config=self.tasks_config["define_scope_and_objectives"],
        )

    @task
    def design_team_structure(self) -> Task:
        return Task(
            config=self.tasks_config["design_team_structure"],
        )

    @task
    def create_project_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_project_plan"],
        )

    @task
    def compile_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["compile_final_report"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
