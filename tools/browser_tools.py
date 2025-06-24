from langchain.tools import tool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from bs4.element import Tag

class BrowserInput(BaseModel):
    website_url: str = Field(description="Complete website URL to scrape and summarize (must include http:// or https://)")

class BrowserTools():
    @tool("scrape_and_summarize_website", args_schema=BrowserInput, return_direct=False)
    @staticmethod
    def scrape_and_summarize_website(website_url: str) -> str:
        """Scrape a website and return a summary of its content. Useful for getting detailed information from specific URLs."""
        
        # Debug logging
        print(f"DEBUG: BrowserTools received URL type: {type(website_url)}")
        print(f"DEBUG: BrowserTools received URL value: {repr(website_url)}")
        
        # Handle empty or invalid input
        if not website_url or not isinstance(website_url, str) or not website_url.strip():
            return "Error: Please provide a valid website URL as a string."
        
        # Clean and validate URL
        url = website_url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Validate URL format
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return "Error: Invalid URL format. Please provide a complete URL."
        except Exception:
            return "Error: Invalid URL format."
        
        try:
            # Set up headers to mimic a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Make the request
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = str(meta_desc.get('content', '')).strip() if isinstance(meta_desc, Tag) else ""
            
            # Extract main content
            # Try to find main content areas
            content_areas = []
            
            # Look for common content containers
            for selector in ['main', 'article', '.content', '#content', '.main-content', '.post-content']:
                elements = soup.select(selector)
                for element in elements:
                    content_areas.append(element.get_text().strip())
            
            # If no specific content areas found, get all paragraphs and headings
            if not content_areas:
                paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                content_areas = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            
            # Clean and combine content
            content_text = ' '.join(content_areas)
            
            # Clean up whitespace and remove empty lines
            content_text = re.sub(r'\s+', ' ', content_text).strip()
            
            # Limit content length for summary
            if len(content_text) > 2000:
                content_text = content_text[:2000] + "..."
            
            # Extract any contact information or important links
            contact_info = []
            
            # Look for phone numbers
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,6}'
            phones = re.findall(phone_pattern, content_text)
            if phones:
                contact_info.append(f"Phone numbers found: {', '.join(phones[:3])}")
            
            # Look for email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, content_text)
            if emails:
                contact_info.append(f"Email addresses: {', '.join(emails[:3])}")
            
            # Build the summary
            summary_parts = [
                f"Website: {url}",
                f"Title: {title_text}",
            ]
            
            if description:
                summary_parts.append(f"Description: {description}")
            
            if content_text:
                summary_parts.append(f"Content Summary: {content_text}")
            
            if contact_info:
                summary_parts.extend(contact_info)
            
            return "\n\n".join(summary_parts)
            
        except requests.exceptions.Timeout:
            return f"Error: Request timeout while accessing {url}. The website may be slow or unresponsive."
        except requests.exceptions.ConnectionError:
            return f"Error: Unable to connect to {url}. Please check the URL and try again."
        except requests.exceptions.HTTPError as e:
            return f"Error: HTTP error {e.response.status_code} while accessing {url}."
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed for {url} - {str(e)}"
        except Exception as e:
            return f"Error: Unable to scrape website {url} - {str(e)}"