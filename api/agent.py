from typing import List, Any
from api.utils import create_chat_message, count_message_tokens, Message
from api.constants import OPENAI_CHAT_MODEL, OPENAI_CHAT_TOKEN_LIMIT, AI_AGENT_ROLE, AI_AGENT_NAME
from api.database import get_last_n_chat_logs
from api.memory import memory

import time

class PromptGenerator:
    def __init__(self) -> None:
        self.constraints: List[str] = []
        self.goals: List[str] = []
        self.name = "Bob"
        self.role = "AI"
        
    def add_constraint(self, constraint: str) -> None:
        self.constraints.append(constraint)
        
    def add_goals(self, goals: str) -> None:
        self.constraints.append(goals)
        
    def set_ai(self, name: str, role: str) -> None:
        self.name = name
        self.role = role
        
    def _generate_numbered_list(self, items: List[Any], item_type="list") -> str:
        """
        Generate a numbered list from given items based on the item_type.

        Args:
            items (list): A list of items to be numbered.
            item_type (str, optional): The type of items in the list.
                Defaults to 'list'.

        Returns:
            str: The formatted numbered list.
        """
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))
    
    def generate_prompt_string(self):
        prompt_string = (
            f"GOALS:\n{self._generate_numbered_list(self.goals)}\n\n"
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
        )
        
        full_prompt = f"You are {self.name}, {self.role}\n{prompt_string}"
        return full_prompt
    
def _get_system_prompt():
    prompt_generator = PromptGenerator()
    
    prompt_generator.set_ai(AI_AGENT_NAME, AI_AGENT_ROLE)
    
    prompt_generator.add_constraint("Always summarize longer answers to prevent long messages. You have 200 characters limit.")
    prompt_generator.add_constraint("Always say good things about the company you work for")
    prompt_generator.add_constraint("Always recommend the products or services from the company you work for")
    prompt_generator.add_constraint("If you don't know the answer. Redirect the user to the website of the company")
    prompt_generator.add_constraint("Do not answer questions or topics that has nothing to do with your company or its products or services")
    prompt_generator.add_constraint("Always answer in the users language")
    
    prompt_generator.add_goals("Introduce yourself and present how you can help the user")
    prompt_generator.add_goals("Help the user answering questions about the products and services")
    prompt_generator.add_goals("Recommend products if make sense")
    
    return prompt_generator.generate_prompt_string()

def generate_context(relevant_memory, chat_history: List[Message], model: str):
    current_context = [
        create_chat_message("system", _get_system_prompt()),
        create_chat_message(
            "system", f"The current time and date is {time.strftime('%c')}"
        ),
    ]
    
    # TODO: Add knowlegde base to query
    
    if relevant_memory != "":
        current_context.append(create_chat_message(
            "system",
            f"This reminds you of these events from your past:\n{relevant_memory}\n\n",
        ))
        
    current_context.extend(chat_history)
    
    total_tokens_used = count_message_tokens(current_context, model=model)
    return current_context, total_tokens_used

def _message_to_string(context: List[Message]) -> str:
    messages = []
    for msg in context:
        messages.append(f"{msg.get('role')}: {msg.get('content')}\n")
        
    return "\n".join(messages)
    
def get_context_with_history(user_id):
    last_history = get_last_n_chat_logs(user_id)
    if len(last_history) > 9:            
        relevant_history_string = _message_to_string(last_history)
        
        last_history_token_count = count_message_tokens(last_history, model=OPENAI_CHAT_MODEL)
    
        limit_send = OPENAI_CHAT_TOKEN_LIMIT - 1500
        
        while last_history_token_count > limit_send and len(last_history) > 0:
            last_history = last_history[1:]
            last_history_token_count = count_message_tokens(last_history, model=OPENAI_CHAT_MODEL)
        
        relevant_memory = memory.get_relevant(relevant_history_string,user_id)
        
        context, current_tokens_used = generate_context(relevant_memory, last_history, model=OPENAI_CHAT_MODEL)
        
        ## TODO: Improve the token limit calculation
        while current_tokens_used > limit_send and len(relevant_memory) > 0:
            ## remove memory to prevent
            relevant_memory = relevant_memory[:-1]
            context, current_tokens_used = generate_context(relevant_memory, last_history, model=OPENAI_CHAT_MODEL)
            
        return context, current_tokens_used
    else:
        return generate_context(last_history, chat_history=[], model=OPENAI_CHAT_MODEL)
    

    
    