import os
    
ENVIRONMENT = os.environ.get('ENVIRONMENT', "development")
CODE_COMMIT = os.environ.get('CODE_COMMIT', "no code commit")
DEPLOYED_AT = os.environ.get('DEPLOYED_AT', "no deployed at")
VERSION = os.environ.get('VERSION', "0.1.0")

AI_AGENT_NAME = os.environ.get('AI_AGENT_NAME', "Bob")
AI_AGENT_ROLE = os.environ.get('AI_AGENT_ROLE', "An AI assistant that help the customers answering questions about the company X")

## open ai LLM
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-3.5-turbo")
OPENAI_CHAT_TOKEN_LIMIT = int(os.getenv("OPENAI_CHAT_TOKEN_LIMIT", 4000))

## database
DATABASE_URL = os.environ.get('DATABASE_URL')

## memory with pinecone
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_API_ENVIRONMENT = os.environ.get("PINECONE_API_ENVIRONMENT")
PINECONE_POD_TYPE = os.environ.get('PINECONE_POD_TYPE', 'p1')
PINECONE_TABLE_NAME = os.environ.get('PINECONE_TABLE_NAME', 'gpt-twilio')

EMBED_DIM = 1536

## twilio credentials
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_ACCOUNT_TOKEN = os.environ.get("TWILIO_ACCOUNT_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
