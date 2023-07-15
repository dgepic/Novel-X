# Novel-X

# Discord Bot

This is a simple Discord bot built with Python and [discord.py](https://discordpy.readthedocs.io/en/stable/). It uses [OpenAI's GPT-3.5](https://openai.com/blog/gpt-3-5/) to generate stories based on user-defined styles and genres.

## Features

- `set` command to store user preferences 
- `novel` command to generate a story based on the user's stored style and genre
- `hello` simple test command

## Setup

### Prerequisites

- Python 3.6+
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [openai](https://github.com/openai/openai-python)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [tinydb](https://github.com/msiemens/tinydb)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/yourname/discord-bot.git
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token and OpenAI API key
   ```
   DISCORD_TOKEN=xxxxxxxxxxxx
   OPENAI_API_KEY=xxxxxxxxxxxx  
   ```
4. Run the bot
   ```py
   python bot.py
   ```

## Usage

- `$set` - Stores user preferences
  - Usage: 
    ```
    $set style humor
    $set genre sci-fi
    ```
- `$novel` - Generates a story based on the user's stored style and genre
- `$hello` - Simple test command

## Acknowledgments

- [discord.py](https://discordpy.readthedocs.io/en/stable/) for the Discord API wrapper
- [OpenAI](https://openai.com/) for the GPT-3.5 API
- [TinyDB](https://github.com/msiemens/tinydb) for simple user data storage

This covers the basic functionality, commands, setup, and usage of the Discord bot. Let me know if you would like me to expand or modify the documentation further.
