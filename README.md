## GPT-4 / GPT-3 for Whatsapp

GPT for Whatsapp is an open-source project that integrates OpenAI GPT-3 and GPT-4 with WhatsApp using the Twilio API. This project allows users to chat with an AI agent through WhatsApp, making it easy for them to get instant responses and assistance.

## Features

- Connects with OpenAI GPT-3 and GPT-4 models
- Supports WhatsApp messaging through the Twilio API
- Stores data reply in PostgreSQL database
- Uses Flask for serving API endpoints
- Integrates with Pinecone for extended memory

## Prerequisites

- Python 3.10+
- PostgreSQL
- A Twilio account (demo account or with a verified WhatsApp number)
- OpenAI API key
- Pinecone API key

## Installation and Configuration

1.  Create a virtual environment and activate it:

`python3 -m venv venv
source venv/bin/activate`

2.  Install the required packages:

`pip install -r requirements.txt`

3.  Set up your environment variables by copying `.env.template` to `.env`:

`cp .env.template .env`

4.  Open the `.env` file and fill in the required information:

````
## AI Assistant
AI_AGENT_NAME=<Your AI Agent Name>
AI_AGENT_ROLE=<Description of the AI Agent's role and company>

## OPENAI LLM
OPENAI_API_KEY=<Your OpenAI API Key>
OPENAI_CHAT_MODEL=gpt-3.5-turbo # or gpt-4, if available
OPENAI_CHAT_TOKEN_LIMIT=4000

## Pinecone Credentials
PINECONE_API_KEY=<Your Pinecone API Key>
PINECONE_API_ENVIRONMENT=<Your Pinecone Environment>
PINECONE_POD_TYPE=p1
PINECONE_TABLE_NAME=gpt-twilio # update if needed

## Twilio Credentials
TWILIO_ACCOUNT_SID=<Your Twilio Account SID>
TWILIO_ACCOUNT_TOKEN=<Your Twilio Account Token>
TWILIO_WHATSAPP_NUMBER=whatsapp:+<Your Verified WhatsApp Number>

## PostgreSQL Database
DATABASE_URL=<Your PostgreSQL Connection String>```

5.  Run the application:

`flask run`

6.  The server will start running at [http://localhost:5000](http://localhost:5000/). You can now use the AI-WhatsApp Assistant by sending a message to your Twilio WhatsApp number.


## Postgres and Pinecone

This project uses postgres to store the user's message to retrieve the last 10 message to include in the context of the chat. Also use these messages to retrieve relevant history from Pinecone.

This will give support for long history

## Contributing

Please feel free to submit issues and pull requests for bug fixes or new features. Make sure to follow the code style and include tests where necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/LICENSE) file for details.
````
