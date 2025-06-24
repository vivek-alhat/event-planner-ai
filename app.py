__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from dotenv import load_dotenv
load_dotenv()

from crewai import Crew
from event_agents import EventAgents, StreamToExpander
from event_tasks import EventTasks
import streamlit as st
import datetime
import sys
import os

st.set_page_config(layout="wide", initial_sidebar_state="expanded")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


class EventCrew:

    def __init__(self, event_description, location, people_count, event_datetime, additional_details, today_str):
        self.event_description = event_description
        self.location = location
        self.people_count = people_count
        self.event_datetime = event_datetime
        self.additional_details = additional_details
        self.today_str = today_str
        self.output_placeholder = st.empty()

    def run(self):
        agents = EventAgents()
        tasks = EventTasks()

        theme_expert = agents.theme_expert()
        agenda_planner = agents.agenda_planner()
        venue_finder = agents.venue_finder()
        travel_logistics_expert = agents.travel_logistics_expert()
        budget_analyst = agents.budget_analyst()

        theme_task = tasks.theme_task(theme_expert, self.event_description, self.additional_details, self.today_str)
        agenda_task = tasks.agenda_task(agenda_planner, self.event_description, self.people_count, self.event_datetime, self.additional_details, self.today_str)
        venue_task = tasks.venue_task(venue_finder, self.location, self.people_count, self.event_datetime, self.additional_details, self.today_str)
        travel_task = tasks.travel_task(travel_logistics_expert, self.location, self.people_count, self.event_datetime, self.additional_details, self.today_str)
        budget_task = tasks.budget_task(budget_analyst, self.location, self.people_count, self.event_datetime, self.additional_details, self.today_str)

        crew = Crew(
            agents=[theme_expert, agenda_planner, venue_finder, travel_logistics_expert, budget_analyst],
            tasks=[theme_task, agenda_task, venue_task, travel_task, budget_task],
            verbose=True
        )

        result = crew.kickoff()
        # Combine all agent/task outputs if available
        if hasattr(result, "tasks_output") and result.tasks_output:
            combined = []
            for i, task_output in enumerate(result.tasks_output):
                # Try to get a readable header for each task
                task_name = crew.tasks[i].description.splitlines()[0].replace(':', '').strip() if hasattr(crew.tasks[i], 'description') else f"Task {i+1}"
                # Each task_output may have .raw or .output or similar
                if hasattr(task_output, "raw"):
                    combined.append(f"### {task_name}\n{task_output.raw}")
                else:
                    combined.append(f"### {task_name}\n{str(task_output)}")
            final_output = "\n\n---\n\n".join(combined)
        else:
            final_output = str(result)
        self.output_placeholder.markdown(final_output)
        return final_output


if __name__ == "__main__":
    # Check for required API keys at startup
    required_keys = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    missing_keys = []
    
    for key in required_keys:
        if not (os.getenv(key)):
            missing_keys.append(key)
    
    if missing_keys:
        st.error(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        st.info("Please add these keys to your environment variables:")
        for key in missing_keys:
            st.code(f"{key} = 'your_api_key_here'")
        st.stop()
    
    # Page header intentionally left empty as per user request
    st.markdown("")
    
    today = datetime.datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')

    with st.sidebar:
        st.header("📋 Plan Your Event")
        st.caption("Fill in the details below to get a comprehensive event plan.")
        
        with st.form("event_form"):
            # Event basics
            st.markdown("#### Event Details")
            event_description = st.text_input(
                "What is the event about? *",
                placeholder="e.g. Annual Sales Meet, Team Building Workshop, Product Launch"
            )
            
            location = st.text_input(
                "Location *",
                placeholder="e.g. Mumbai, Delhi NCR, Bangalore"
            )
            
            people_count = st.number_input(
                "Number of Attendees *",
                min_value=1,
                max_value=1000,
                step=1,
                value=50
            )
            
            # Date and time
            st.markdown("#### When")
            date_input = st.date_input(
                "Event Date *",
                min_value=today,
                format="DD/MM/YYYY"
            )
            time_input = st.time_input(
                "Start Time *",
                value=datetime.time(9, 0)
            )
            
            # Additional requirements
            st.markdown("#### Special Requirements")
            additional_details = st.text_area(
                "Special requests or notes",
                placeholder="e.g. Vegetarian catering, AV equipment, accessibility needs, team building activities, specific themes",
                height=100
            )
            
            submitted = st.form_submit_button("🚀 Generate Event Plan", use_container_width=True)
            
        # Sidebar info
        st.markdown("---")
        st.markdown("### 🤖 What our AI does:")
        st.markdown("""
        - **Theme Expert**: Suggests creative themes using web search
        - **Agenda Planner**: Creates detailed schedules with research
        - **Venue Finder**: Finds and analyzes venues with web scraping
        - **Travel Expert**: Plans logistics with current information
        - **Budget Analyst**: Calculates costs in INR with real-time data
        """)


    if submitted:
        # Validation
        if not event_description.strip():
            st.error("❌ Please describe what your event is about.")
            st.stop()
        
        if not location.strip():
            st.error("❌ Please specify the event location.")
            st.stop()
        
        if people_count <= 0:
            st.error("❌ Please specify a valid number of attendees.")
            st.stop()
        
        # Ensure date_input and time_input are single values, not tuples
        if isinstance(date_input, tuple):
            date_input = date_input[0] if date_input else None
        if isinstance(time_input, tuple):
            time_input = time_input[0] if time_input else None
        
        if date_input is None or time_input is None:
            st.error("❌ Please select a valid date and time.")
            st.stop()
        
        # Show event summary
        event_datetime = f"{date_input.strftime('%Y-%m-%d')} {time_input.strftime('%H:%M')}"
        
        st.markdown("### 📝 Event Summary")
        with st.expander("Click to view event details", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Event:** {event_description}")
                st.write(f"**Location:** {location}")
            with col2:
                st.write(f"**Attendees:** {people_count}")
                st.write(f"**Date:** {date_input.strftime('%d %B %Y')}")
            with col3:
                st.write(f"**Time:** {time_input.strftime('%I:%M %p')}")
                if additional_details.strip():
                    st.write(f"**Special Notes:** {additional_details[:100]}...")
        
        # Run the AI agents with enhanced error handling
        with st.status("🤖 **AI Agents are working on your event...**", state="running", expanded=True) as status:
            with st.container(height=400, border=False):
                try:
                    # Display agent progress
                    st.write("🔍 **Theme Expert**: Researching creative themes...")
                    st.write("📅 **Agenda Planner**: Designing event schedule...")
                    st.write("🏢 **Venue Finder**: Searching and analyzing venues...")
                    st.write("🚗 **Travel Expert**: Planning logistics...")
                    st.write("💰 **Budget Analyst**: Calculating costs...")
                    st.write("---")
                    
                    sys.stdout = StreamToExpander(st)
                    event_crew = EventCrew(event_description, location, people_count, event_datetime, additional_details, today_str)
                    result = event_crew.run()
                    
                    if not result:
                        st.error("No event plan was generated. Please try again.")
                        st.stop()
                        
                except Exception as e:
                    st.error(f"An error occurred while generating the event plan: {str(e)}")
                    st.error("This might be due to:")
                    st.error("- API rate limits or connectivity issues")
                    st.error("- Invalid API keys")
                    st.error("- Temporary service unavailability")
                    st.info("Please check your API keys and try again in a few moments.")
                    st.stop()
                finally:
                    sys.stdout = sys.__stdout__  # Reset stdout
                
            status.update(label="✅ Event Plan Ready!", state="complete", expanded=False)

        # Display results
        st.markdown("---")
        # Align heading and download button on the same line
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown("## 🎊 Your Complete Event Plan")
        # Convert result to string for download and display
        result_str = str(result)
        st.session_state["event_plan_result"] = result_str  # Persist in session state
        with col2:
            if st.download_button(
                label="Download",
                data=result_str,
                file_name=f"event_plan_{event_description.replace(' ', '_').lower()}_{date_input.strftime('%Y%m%d')}.md",
                mime="text/markdown"
            ):
                st.success("Plan downloaded!")
        
        # Display the plan with enhanced formatting
        try:
            if isinstance(result, str) and result.strip():
                st.markdown(result_str)
            else:
                st.warning("The event plan was generated but may be incomplete. Please try generating again.")
        except Exception as e:
            st.error(f"Error displaying the plan: {str(e)}")
            st.text_area("Raw Plan Output:", value=result_str, height=400)

    # If not submitted, but a plan exists in session_state, show it
    elif "event_plan_result" in st.session_state:
        st.markdown("---")
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown("## 🎊 Your Complete Event Plan")
        with col2:
            st.download_button(
                label="Download",
                data=st.session_state["event_plan_result"],
                file_name="event_plan.md",
                mime="text/markdown"
            )
        st.markdown(st.session_state["event_plan_result"])