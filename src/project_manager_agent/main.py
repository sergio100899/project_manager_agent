import argparse
from datetime import datetime
from crew import ProjectManagerCrew


def run(project_description: str):
    today_str = datetime.today().strftime("%Y-%m-%d")

    inputs = {
        "project_description": project_description,
        "today": today_str,
    }

    crew_instance = ProjectManagerCrew()
    crew = crew_instance.crew()
    result = crew.kickoff(inputs=inputs)

    print(result)
    print(crew.usage_metrics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "project_description",
        type=str,
        help="Project Description with one sentence (in quotes)",
    )
    args = parser.parse_args()

    run(args.project_description)
