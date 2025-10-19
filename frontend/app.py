import io
import sys
import os
import base64
import zipfile
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

sys.path.append(os.path.abspath("../src"))

from project_manager_agent.crew import ProjectManagerCrew

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "output")

today_str = datetime.today().strftime("%Y-%m-%d")

st.markdown(
    """
    <style>
        /* General background and text colors */
        .main {
            background-color: black;
            color: white;
        }

        /* Text input styling */
        .stTextInput > div > div > input {
            background-color: #333 !important;
            color: white !important;
        }

        /* Main container with 10% padding on top and sides */
        .block-container {
            padding-left: 10% !important;
            padding-right: 10% !important;
            padding-top: 10% !important;
            padding-bottom: 2% !important; /* optional: less padding at the bottom */
            max-width: 100% !important;
        }

        /* Tabs should take up full width within the padded area */
        .stTabs [role="tablist"] {
            max-width: 100% !important;
        }

        /* Ensure embedded HTML components take full width */
        iframe {
            width: 100% !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("AI Project Manager Agent")
project_description = st.text_input("Describe your project with one sentence:")

run_finished_successfully = False
st.session_state.stop_requested = st.session_state.get("stop_requested", False)

# Buttons setup

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    run_button = st.button("Run Project Crew")
with col2:
    stop_button = st.button("Stop Analysis")

progress_bar = st.progress(0)
status_text = st.empty()
log_area = st.empty()
html_preview_area = st.empty()

task_counter = {"completed": 0}

friendly_names = {
    "project_strategist": "Strategy Specialist",
    "team_architect": "Team Architect",
    "project_planner": "Project Planner",
    "technology_architect": "Architecture Specialist",
    "visual_diagram_designer": "Visual Designer",
    "pmo_reporter": "PMO Analyst",
}

tabs_labels = ["Final Output", "Architecture Diagram", "Gantt Chart"]
tabs = st.tabs(tabs_labels)
output_tab, arch_tab, gantt_tab = tabs

output_area = output_tab.empty()
arch_area = arch_tab.empty()
gantt_area = gantt_tab.empty()


arch_file = os.path.join(output_dir, "architecture.html")
gantt_file = os.path.join(output_dir, "gantt.html")


def stream_callback(output):
    if st.session_state.stop_requested:
        raise Exception("Analysis stopped by user")

    agent_role = getattr(output.agent, "role", str(output.agent))
    agent_role = friendly_names.get(agent_role, agent_role)

    # Progress bar
    task_counter["completed"] += 1
    total_tasks = len(crew.tasks)
    percent = int(task_counter["completed"] / total_tasks * 100)

    gif_path = os.path.join(script_dir, "assets", "loading.gif")
    with open(gif_path, "rb") as f:
        gif_base64 = base64.b64encode(f.read()).decode()

    html_status = f"""
    <div style="display:flex; align-items:center; font-size:24px; color:white;">
        <img src="data:image/gif;base64,{gif_base64}" width="50">
        <span style="margin-right:15px;">Analyzing with {agent_role}...</span>
    </div>
    """
    status_text.markdown(html_status, unsafe_allow_html=True)
    progress_bar.progress(percent)
    log_area.text(f"Completed: {agent_role} ({percent}%)")

    # Show html diagram once are generated
    if os.path.exists(arch_file):
        with arch_area:
            with open(arch_file, "r", encoding="utf-8") as f:
                html_content = f.read()
                components.html(
                    html_content,
                    height=600,
                    scrolling=True,
                )

    if os.path.exists(gantt_file):
        with gantt_area:
            with open(gantt_file, "r", encoding="utf-8") as f:
                html_content = f.read()
                components.html(
                    html_content,
                    height=600,
                    scrolling=True,
                )


if run_button:
    st.session_state.stop_requested = False
    if not project_description.strip():
        st.warning("Please enter a project description first.")
    else:
        crew_instance = ProjectManagerCrew()
        crew = crew_instance.crew()

        # Callbacks for progress bar
        for task_obj in crew.tasks:
            task_obj.callback = stream_callback

        # Files empty templates
        for file_path in [arch_file, gantt_file]:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("<html></html>")

        md_files = ["report.md", "schedule.md", "architecture.md"]
        for filename in md_files:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")

        result = None

        try:
            result = crew.kickoff(
                inputs={"project_description": project_description, "today": today_str}
            )
            progress_bar.progress(100)
            status_text.write("All agents completed!")
            st.session_state.run_finished_successfully = True
        except Exception as e:
            status_text.write(f"Error: {str(e)}")
            st.session_state.run_finished_successfully = False

        log_area.text("")

        with output_tab:
            st.subheader("Project Analysis")
            if st.session_state.get("run_finished_successfully", False) and result:
                st.markdown(result, unsafe_allow_html=True)
            elif st.session_state.stop_requested:
                st.warning("Analysis was stopped by the user.")
            else:
                st.info("Project output will appear here after running the crew.")

# Download button

with col3:
    if (
        st.session_state.get("run_finished_successfully", False)
        and not st.session_state.stop_requested
    ):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zip_file.write(file_path, arcname=arcname)
        zip_buffer.seek(0)
        st.download_button(
            label="Download Output",
            data=zip_buffer,
            file_name="project_output.zip",
            mime="application/zip",
        )
