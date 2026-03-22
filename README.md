# Telegram Bot — RabbitMQ Consumer

A message pipeline that listens to a RabbitMQ queue and forwards every incoming message to a Telegram chat. The publisher enqueues JSON payloads; the consumer picks them up and dispatches them via the Telegram Bot API.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.x-FF6600?logo=rabbitmq&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot_API-blue?logo=telegram&logoColor=white)

---

## Architecture

```
[Publisher] ──► [RabbitMQ Exchange] ──► [Queue] ──► [Consumer] ──► [Telegram Bot API] ──► [Chat]
```

The publisher sends a JSON payload to a durable exchange. The consumer runs a blocking loop, receives each message, and delegates delivery to the Telegram driver. The driver reads credentials from environment variables and POSTs to the Bot API.

---

## Stack

- Python 3.10+
- [Pika](https://pika.readthedocs.io/) — RabbitMQ AMQP client
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variable management
- [Requests](https://docs.python-requests.org/) — HTTP client for the Telegram API
- RabbitMQ (local or via Docker)

---

## Getting Started

### Prerequisites

- Python 3.10+
- RabbitMQ running on `localhost:5672` (default guest credentials)

```bash
# Start RabbitMQ with Docker
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### Setup

```bash
# Clone the repository
git clone https://github.com/eduardoperorck/telegram-bot-python-rabbitmq.git
cd telegram-bot-python-rabbitmq

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
```

Edit `.env` with your Telegram credentials:

```env
TELEGRAM_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

> To get a bot token, talk to [@BotFather](https://t.me/BotFather) on Telegram.
> To get your chat ID, forward a message to [@userinfobot](https://t.me/userinfobot).

### Running

```bash
# Start the consumer (listens to the queue and forwards to Telegram)
python -m src.main.rabbitmq_configs.consumer

# In a separate terminal, publish a test message
python publisher.py
```

The expected message payload is:

```json
{ "msg": "Hello from RabbitMQ!" }
```

---

## Project Structure

```
├── publisher.py                        # RabbitMQ publisher — sends messages to the exchange
├── sender.py                           # Standalone Telegram sender (for testing)
├── requirements.txt
├── .env.example
└── src/
    ├── drivers/
    │   └── telegram_sender.py          # Telegram Bot API driver (reads from .env)
    └── main/
        └── rabbitmq_configs/
            ├── callback.py             # Message callback — parses JSON and calls telegram_sender
            └── consumer.py             # RabbitMQ consumer — declares queue and starts consuming
```

---

## Environment Variables

| Variable           | Description                            |
|--------------------|----------------------------------------|
| `TELEGRAM_TOKEN`   | Bot token from BotFather               |
| `TELEGRAM_CHAT_ID` | Target chat, group, or channel ID      |

---

## Message Format

The publisher must send a JSON body with the following structure:

```json
{
  "msg": "your message text here"
}
```

The callback extracts the `msg` field and sends it as plain text to the configured Telegram chat.
