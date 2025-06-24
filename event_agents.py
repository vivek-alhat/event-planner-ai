from crewai import Agent
import re
import streamlit as st
from langchain_community.llms import OpenAI
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

class EventAgents():
    def __init__(self):
        # Initialize tool instances
        self.search_tools = SearchTools()
        self.calculator_tools = CalculatorTools()
        self.browser_tools = BrowserTools()
    
    def theme_expert(self):
        return Agent(
            role='Theme Expert',
            goal='Suggest creative and relevant event themes based on the event description and company culture',
            backstory='An expert in corporate event themes and branding with extensive knowledge of current trends and creative concepts.',
            tools=[
                self.search_tools.search_internet,
            ],
            verbose=True,
            max_iter=3,  # Limit iterations to prevent loops
            max_execution_time=120,  # Timeout after 2 minutes
        )

    def agenda_planner(self):
        return Agent(
            role='Agenda Planner',
            goal='Design a detailed agenda based on event type, goals, and people count',
            backstory='A professional event manager with 10+ years of experience in planning corporate event schedules and optimizing attendee engagement.',
            tools=[
                self.search_tools.search_internet,
            ],
            verbose=True,
            max_iter=3,
            max_execution_time=120,
        )

    def venue_finder(self):
        return Agent(
            role='Venue Finder',
            goal='Find and summarize the best venues in the given location for the event',
            backstory='A venue sourcing specialist with deep knowledge of event spaces, capacity requirements, and venue amenities across different locations.',
            tools=[
                self.search_tools.search_internet,
                self.browser_tools.scrape_and_summarize_website,
            ],
            verbose=True,
            max_iter=4,  # Allow more iterations for venue research
            max_execution_time=180,  # 3 minutes for venue research
        )

    def travel_logistics_expert(self):
        return Agent(
            role='Travel & Logistics Expert',
            goal='Suggest travel options for attendees to reach the venue efficiently',
            backstory='A logistics coordinator specializing in corporate events with expertise in transportation planning and cost-effective travel solutions.',
            tools=[
                self.search_tools.search_internet,
            ],
            verbose=True,
            max_iter=3,
            max_execution_time=120,
        )

    def budget_analyst(self):
        return Agent(
            role='Budget Analyst',
            goal='Estimate the total event cost in INR, including venue, travel, food, and other expenses',
            backstory='A finance expert with 8+ years of experience in event budgeting, cost estimation, and financial planning for corporate events.',
            tools=[
                self.calculator_tools.calculate,
                self.search_tools.search_internet,
            ],
            verbose=True,
            max_iter=4,  # Allow more iterations for complex calculations
            max_execution_time=150,  # 2.5 minutes for budget analysis
        )

class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'"task"\s*:\s*"(.*?)"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        # Remove st.toast to avoid annoying toasts
        # if task_value:
        #     st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary
            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Theme Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("Theme Expert", f":{self.colors[self.color_index]}[Theme Expert]")
        if "Agenda Planner" in cleaned_data:
            cleaned_data = cleaned_data.replace("Agenda Planner", f":{self.colors[self.color_index]}[Agenda Planner]")
        if "Venue Finder" in cleaned_data:
            cleaned_data = cleaned_data.replace("Venue Finder", f":{self.colors[self.color_index]}[Venue Finder]")
        if "Travel & Logistics Expert" in cleaned_data:
            cleaned_data = cleaned_data.replace("Travel & Logistics Expert", f":{self.colors[self.color_index]}[Travel & Logistics Expert]")
        if "Budget Analyst" in cleaned_data:
            cleaned_data = cleaned_data.replace("Budget Analyst", f":{self.colors[self.color_index]}[Budget Analyst]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []