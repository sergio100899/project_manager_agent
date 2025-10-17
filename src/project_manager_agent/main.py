from crew import ProjectManagerCrew


def run():
    inputs = {"project_description": "Un buscador inteligente de jurisprudencia"}
    crew_instance = ProjectManagerCrew()
    crew = crew_instance.crew()
    result = crew.kickoff(inputs=inputs)
    print("Done:", result)


if __name__ == "__main__":
    run()
