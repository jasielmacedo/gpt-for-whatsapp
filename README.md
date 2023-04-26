## GPT-4 / GPT-3 for Whatsapp

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jasielmacedo/gpt-for-whatsapp)

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

```
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
DATABASE_URL=<Your PostgreSQL Connection String>
```

5.  Run the application:

`flask run`

6.  The server will start running at [http://localhost:5000](http://localhost:5000/). You can now use the AI-WhatsApp Assistant by sending a message to your Twilio WhatsApp number.

## Configuring Twilio Account

To set up a free Twilio account and configure it for the AI-WhatsApp Assistant, follow these steps:

1.  Sign up for a free Twilio account at [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).
2.  Once your account is created and you're logged in, navigate to the [Twilio Console](https://www.twilio.com/console).
3.  Configure the whatsapp API on `Develop > Messaging > Try it out > Send a Whatsapp Message`
4.  Go to the 'Sandbox Settings' section and configure the webhook for incoming messages. This repo will provide `https://yourserver.com/chat` and `https://yourserver.com/status_check` to use as webhook.
5.  Save the changes by clicking on the 'Save' button at the bottom of the page.
6.  In the Twilio Console, navigate to the 'Settings' > 'WhatsApp Sandbox' section.
7.  Follow the instructions to link your WhatsApp account to the Twilio Sandbox. Send the provided code from your WhatsApp account to the Twilio Sandbox number.
8.  Once your WhatsApp number is linked to the Twilio Sandbox, you can use it to send messages to the AI WhatsApp Assistant.
9.  Don't forget to update the `.env` file in your project with your Twilio Account SID, Account Token, and WhatsApp number.

## Postgres and Pinecone

This project uses postgreSQL to store the user's message and AI replies to retrieve the last 10 message to include in the context of the chat. Also use these messages to retrieve relevant history from Pinecone.

Since pinecone we can't retrieve messages based on datetime, postgreSQL seem a good option for that

This will give support for long history

## Contributing

Please feel free to submit issues and pull requests for bug fixes or new features. Make sure to follow the code style and include tests where necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/jasielmacedo/gpt-for-whatsapp/blob/main/LICENSE) file for details.

```

```
