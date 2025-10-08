import os
from dotenv import load_dotenv

def load_key():
    """
    从.env文件中加载 API Key
    return: str
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # Check if environment variables are present
    if not api_key:
        raise ValueError("Environment variables \"DASHSCOPE_API_KEY\" are missing.")

    # Return environment variables as dictionary
    return api_key