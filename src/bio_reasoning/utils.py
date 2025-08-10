from typing import Any, Dict, List

import httpx


def query_chat_completion(
    base_url: str,
    api_key: str,
    model_name: str,
    messages: List[Dict[str, Any]],
    timeout: int = 600,
) -> str:
    """
    Sends a chat completion request to an external API.

    Args:
        base_url (str): Base URL of the API service.
        api_key (str): API key for authentication.
        model_name (str): Name of the model to use for chat completions.
        messages (List[Dict[str, str | List[Dict[str, str]]]]): List of message objects describing the conversation.
        timeout (int, optional): Timeout for the request in seconds. Defaults to 600.

    Returns:
        str: The content of the API's response.

    Raises:
        RuntimeError: If the API request fails with an HTTP error.
    """
    api_url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {"model": model_name, "messages": messages}

    try:
        response = httpx.post(api_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Failed to get chat completion: {e.response.text}") from e
