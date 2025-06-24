import json
import os
import requests
import streamlit as st
from langchain.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query string to find information on the internet")

class SearchTools():
    @tool("search_internet", args_schema=SearchInput, return_direct=False)
    @staticmethod
    def search_internet(query: str) -> str:
        """Useful to search the internet about a given topic and return relevant results. Input should be a search query string."""
        
        # Debug logging
        print(f"DEBUG: SearchTools received query type: {type(query)}")
        print(f"DEBUG: SearchTools received query value: {repr(query)}")
        
        # Handle empty or invalid input
        if not query or not isinstance(query, str) or not query.strip():
            return "Error: Please provide a valid search query as a string."
        
        # Check for API key
        try:
            api_key = os.getenv('SERPER_API_KEY')
            if not api_key:
                return "Error: SERPER_API_KEY not configured. Please add it to your Streamlit secrets or environment variables."
        except Exception:
            return "Error: Unable to access API key configuration."
        
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query.strip()})
        headers = {
            'X-API-KEY': api_key,
            'content-type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            
            response_data = response.json()
            
            # Check if there are organic results
            if 'organic' not in response_data or not response_data['organic']:
                return "No search results found. Please try a different query."
            
            results = response_data['organic']
            formatted_results = []
            
            for result in results[:top_result_to_return]:
                try:
                    formatted_results.append('\n'.join([
                        f"Title: {result.get('title', 'N/A')}", 
                        f"Link: {result.get('link', 'N/A')}",
                        f"Snippet: {result.get('snippet', 'N/A')}", 
                        "\n-----------------"
                    ]))
                except Exception as e:
                    continue

            if not formatted_results:
                return "No valid search results could be formatted."
            
            return '\n'.join(formatted_results)
            
        except requests.RequestException as e:
            return f"Error: Failed to perform search - {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response from search service."
        except Exception as e:
            return f"Error: Unexpected error during search - {str(e)}"