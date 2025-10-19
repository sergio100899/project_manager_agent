from crewai import Agent, Crew, Process, Task, TaskOutput
from crewai.project import CrewBase, agent, crew, task

from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from project_manager_agent.tools.html_tool import CleanHTMLTool

from crewai import LLM

# LLM models

llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.8,
)

llm_pro = LLM(
    model="gemini/gemini-2.5-pro",
    temperature=0.5,
)


def callback_function(output: TaskOutput):
    print(f"""
        Task completed!
        Agent: {output.agent}
    """)


@CrewBase
class ProjectManagerCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    # Agents configurations

    @agent
    def project_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["project_strategist"],
            verbose=True,
            cache=False,
            llm=llm,
            max_execution_time=70,
        )

    @agent
    def team_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["team_architect"],
            verbose=True,
            cache=False,
            llm=llm,
            max_execution_time=70,
        )

    @agent
    def project_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["project_planner"],
            verbose=True,
            cache=False,
            llm=llm,
            max_execution_time=110,
        )

    @agent
    def technology_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["technology_architect"],
            verbose=True,
            cache=False,
            llm=llm,
            max_retries=3,
            max_execution_time=140,
        )

    @agent
    def visual_diagram_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["visual_diagram_designer"],
            verbose=True,
            cache=False,
            llm=llm_pro,
            reasoning=True,
            max_retries=3,
            max_execution_time=150,
        )

    @agent
    def pmo_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["pmo_reporter"],
            verbose=True,
            llm=llm_pro,
            cache=False,
            reasoning=True,
            max_retries=3,
            max_execution_time=120,
        )

    # Tasks configurations

    @task
    def define_scope_and_objectives(self) -> Task:
        return Task(
            config=self.tasks_config["define_scope_and_objectives"],
            callback=callback_function,
        )

    @task
    def design_team_structure(self) -> Task:
        return Task(
            config=self.tasks_config["design_team_structure"],
            callback=callback_function,
        )

    @task
    def create_project_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_project_plan"], callback=callback_function
        )

    @task
    def design_technology_architecture(self) -> Task:
        return Task(
            config=self.tasks_config["design_technology_architecture"],
            callback=callback_function,
        )

    @task
    def generate_architecture_html(self) -> Task:
        return Task(
            config=self.tasks_config["generate_architecture_html"],
            tools=[CleanHTMLTool()],
            callback=callback_function,
        )

    @task
    def generate_gantt_html(self) -> Task:
        return Task(
            config=self.tasks_config["generate_gantt_html"],
            tools=[CleanHTMLTool()],
            callback=callback_function,
        )

    @task
    def compile_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["compile_final_report"], callback=callback_function
        )

    # Crew configuration

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
