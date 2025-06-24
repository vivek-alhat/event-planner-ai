import os
import streamlit as st
from typing import Optional

class Config:
    """Configuration management for Event Planner Agent"""
    
    @staticmethod
    def get_api_key(key_name: str) -> Optional[str]:
        """
        Get API key from environment variables
        Priority: Environment variables
        """
       
        
        # Fallback to environment variables
        return os.getenv(key_name)
    
    @staticmethod
    def get_openai_config() -> dict:
        """Get OpenAI configuration"""
        return {
            'api_key': Config.get_api_key('OPENAI_API_KEY'),
            'model': Config.get_api_key('OPENAI_MODEL') or 'gpt-4-turbo-preview',
            'temperature': float(Config.get_api_key('OPENAI_TEMPERATURE') or '0.7')
        }
    
    @staticmethod
    def get_serper_config() -> dict:
        """Get Serper API configuration"""
        return {
            'api_key': Config.get_api_key('SERPER_API_KEY'),
            'max_results': int(Config.get_api_key('SERPER_MAX_RESULTS') or '4')
        }
    
    @staticmethod
    def get_browserless_config() -> dict:
        """Get Browserless API configuration"""
        return {
            'api_key': Config.get_api_key('BROWSERLESS_API_KEY'),
            'timeout': int(Config.get_api_key('BROWSERLESS_TIMEOUT') or '30')
        }
    
    @staticmethod
    def validate_required_keys() -> tuple[bool, list[str]]:
        """
        Validate that all required API keys are present
        Returns: (is_valid, missing_keys)
        """
        required_keys = [
            'OPENAI_API_KEY',
            'SERPER_API_KEY', 
            'BROWSERLESS_API_KEY'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not Config.get_api_key(key):
                missing_keys.append(key)
        
        return len(missing_keys) == 0, missing_keys
    
    @staticmethod
    def get_app_config() -> dict:
        """Get general application configuration"""
        return {
            'max_attendees': int(Config.get_api_key('MAX_ATTENDEES') or '1000'),
            'default_attendees': int(Config.get_api_key('DEFAULT_ATTENDEES') or '50'),
            'enable_feedback': Config.get_api_key('ENABLE_FEEDBACK') != 'false',
            'enable_download': Config.get_api_key('ENABLE_DOWNLOAD') != 'false'
        }