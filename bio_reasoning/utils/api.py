import time
import random
import logging
from typing import Dict, Any, Optional
import openai
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def call_model_with_retry(
    messages: list,
    model_name: str = MODEL_NAME,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 8.0,
    timeout: float = 30.0,
) -> Optional[Dict[str, Any]]:
    """Call the model with exponential backoff retry logic."""
    client = openai.OpenAI(base_url=MODEL_BASE_URL, api_key=MODEL_API_KEY, timeout=timeout)
    delay = initial_delay

    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries} to call model {model_name}")
            logger.debug(f"Messages: {messages}")
            logger.debug(f"Using base URL: {MODEL_BASE_URL}")
            logger.debug(f"Using API key: {MODEL_API_KEY[:4]}...")
            
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                timeout=timeout
            )
            
            logger.debug(f"Response received: {response.choices[0].message.content[:100]}...")
            return {
                "content": response.choices[0].message.content,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error on attempt {attempt + 1}/{max_retries}: {e}")
            if attempt == max_retries - 1:  # Last attempt
                logger.error(f"Failed after {max_retries} attempts")
                return {
                    "content": "Error: Unable to get response from model",
                    "success": False
                }
            
            # Add jitter to the delay
            jitter = random.uniform(0, 0.1 * delay)
            sleep_time = min(delay + jitter, max_delay)
            logger.info(f"Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            delay *= 2  # Exponential backoff 