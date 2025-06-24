from crewai import Task
from textwrap import dedent
from datetime import date

class EventTasks():
    def theme_task(self, agent, event_description, additional_details, today_str):
        return Task(
            description=dedent(f"""
                Today's date: {today_str}
                
                You are tasked with suggesting creative and relevant event themes for a corporate event.
                
                Event Description: {event_description}
                Additional Details: {additional_details}
                
                Please research current event theme trends and suggest 3-5 creative themes that would be appropriate for this corporate event.
                Consider the company culture, event type, and any specific requirements mentioned.
                
                For each theme suggestion, provide:
                1. Theme name
                2. Brief description of the theme concept
                3. Key decorative elements or color schemes
                4. Why this theme fits the event description
                
                When using the search tool, always provide your query as a JSON string in this format:
                {{"query": "your search query here"}}
                Example: {{"query": "creative office party themes 2025"}}
            """),
            expected_output="A detailed list of 3-5 creative event theme suggestions with descriptions, decorative elements, and rationale for each theme.",
            agent=agent
        )

    def agenda_task(self, agent, event_description, people_count, event_datetime, additional_details, today_str):
        return Task(
            description=dedent(f"""
                Today's date: {today_str}
                
                You are tasked with creating a detailed agenda for a corporate event.
                
                Event Description: {event_description}
                People Count: {people_count}
                Event Date & Time: {event_datetime}
                Additional Details: {additional_details}
                
                Create a comprehensive agenda that includes:
                1. Welcome and registration
                2. Main activities/sessions appropriate for the event type
                3. Networking opportunities
                4. Break times and meals
                5. Closing activities
                
                Consider the number of attendees and duration when planning activities.
                Research best practices for similar corporate events to ensure engaging content.
                
                When using the search tool, always provide your query as a JSON string in this format:
                {{"query": "your search query here"}}
                Example: {{"query": "corporate event agenda template"}}
            """),
            expected_output="A detailed, time-based agenda for the event with specific activities, duration, and logistics for each segment.",
            agent=agent
        )

    def venue_task(self, agent, location, people_count, event_datetime, additional_details, today_str):
        return Task(
            description=dedent(f"""
                Today's date: {today_str}
                
                You are tasked with finding suitable venues for a corporate event.
                
                Location: {location}
                People Count: {people_count}
                Event Date & Time: {event_datetime}
                Additional Details: {additional_details}
                
                Find and research 3-5 suitable venues in the specified location that can accommodate the number of attendees.
                
                For each venue, provide:
                1. Venue name and location
                2. Capacity details
                3. Amenities and facilities available
                4. Approximate pricing (if available)
                5. Contact information
                6. Why this venue is suitable for the event
                
                Use the search tool to find venues, then use the browser tool to get detailed information from venue websites.
                
                When using the search tool, always provide your query as a JSON string in this format:
                {{"query": "your search query here"}}
                Example: {{"query": "corporate event venues {location}"}}
                
                When using the browser tool, provide complete URLs starting with https://
            """),
            expected_output="A comprehensive list of 3-5 suitable venues with detailed information including capacity, amenities, pricing, and contact details.",
            agent=agent
        )

    def travel_task(self, agent, location, people_count, event_datetime, additional_details, today_str):
        return Task(
            description=dedent(f"""
                Today's date: {today_str}
                
                You are tasked with suggesting travel options for event attendees.
                
                Location: {location}
                People Count: {people_count}
                Event Date & Time: {event_datetime}
                Additional Details: {additional_details}
                
                Research and suggest various travel options for attendees to reach the event venue:
                
                1. Local transportation (within the city)
                2. Inter-city options (if attendees are coming from other cities)
                3. Airport transfers (if applicable)
                4. Group transportation options
                5. Public transportation alternatives
                
                Consider cost-effectiveness, convenience, and the number of attendees.
                Provide estimated travel times and any booking recommendations.
                
                Important: Do NOT include actual transportation costs in your recommendations, as these will be handled separately by attendees.
                
                When using the search tool, always provide your query as a JSON string in this format:
                {{"query": "your search query here"}}
                Example: {{"query": "transportation options {location}"}}
            """),
            expected_output="Comprehensive travel recommendations including local transport, inter-city options, and group transportation suggestions with estimated travel times.",
            agent=agent
        )

    def budget_task(self, agent, location, people_count, event_datetime, additional_details, today_str):
        return Task(
            description=dedent(f"""
                Today's date: {today_str}
                
                You are tasked with creating a detailed budget estimate for a corporate event.
                
                Location: {location}
                People Count: {people_count}
                Event Date & Time: {event_datetime}
                Additional Details: {additional_details}
                
                Create a comprehensive budget estimate in INR that includes:
                
                1. Venue rental costs
                2. Catering (meals, snacks, beverages)
                3. Audio/Visual equipment
                4. Decorations and theme setup
                5. Entertainment/speakers (if applicable)
                6. Photography/videography
                7. Stationery and materials
                8. Miscellaneous expenses (10-15% buffer)
                
                IMPORTANT: Do NOT include transportation or travel costs as these will be handled by individual attendees.
                
                Research current market rates in the specified location and use the calculator tool for all mathematical computations.
                
                When using the search tool, always provide your query as a JSON string in this format:
                {{"query": "your search query here"}}
                Example: {{"query": "corporate event costs {location} per person"}}
                
                For calculations, use simple expressions like:
                - "250 * 100" (for per person costs)
                - "15000 + 25000 + 10000" (for adding different cost components)
            """),
            expected_output="A detailed budget breakdown in INR with itemized costs for all event components (excluding transportation), total estimated cost, and cost per person.",
            agent=agent
        )