import pandas as pd
import json
import openai
import tiktoken
import time

from typing import List, Dict, TypedDict
from time import sleep
from loguru import logger
        
def load_data_from_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)
    
def load_data_from_txt(file_name):
    with open(file_name, 'r') as file:
        return file.read()
    
def dalle_image_generation(prompt, size = "256x256"):
  try:
      response = openai.Image.create(
          prompt=prompt,
          n=1,
          size=size,
      )
      return response["data"][0]["url"]
  except Exception as oops:
      print('Error communicating with OpenAI:', oops)
    
def create_chat_completion(messages: List[Dict[str, str]], model=None, temperature=1, max_tokens=None)->str:
    """Create a chat completion using the OpenAI API"""
    response = None
    num_retries = 5
    for attempt in range(num_retries):
        try:
            response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            break
        except openai.error.RateLimitError:
            logger.error("Error: API Rate Limit Reached.")
            time.sleep(1)
        except openai.error.APIError as e:
            if e.http_status == 502:
                logger.error("Error: ", "API Bad gateway.")
                time.sleep(1)
            else:
                raise
            if attempt == num_retries - 1:
                raise

    if response is None:
        raise RuntimeError("Failed to get response after 5 retries")

    return response.choices[0].message["content"]
            
def get_ada_embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]

# This file includes code from Auto-GPT, which is licensed
# under the MIT license. The original code can be found at https://github.com/Significant-Gravitas/Auto-GPT

class Message(TypedDict):
    """OpenAI Message object containing a role and the message content"""

    role: str
    content: str
    
def create_chat_message(role, content) -> Message:
    return {"role": role, "content": content}

def count_message_tokens(messages : List[Dict[str, str]] | List[Message], model : str = "gpt-3.5-turbo-0301") -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
    messages (list): A list of messages, each of which is a dictionary containing the role and content of the message.
    model (str): The name of the model to use for tokenization. Defaults to "gpt-3.5-turbo-0301".

    Returns:
    int: The number of tokens used by the list of messages.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # !Node: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return count_message_tokens(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        # !Note: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return count_message_tokens(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
    string (str): The text string.
    model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
    int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens