
import discord
from discord.ext import commands
import openai
import os
import re

from dotenv import load_dotenv
load_dotenv()

from tinydb import TinyDB, Query
db = TinyDB('db.json')
users = db.table('users')

openai.api_key = os.getenv("OPENAI_API_KEY")

token = os.getenv('DISCORD_TOKEN')
print(token)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Helper functions
def save_user_data(user_id, key, value):
    User = Query()
    user_entry = users.get(User.user_id == user_id)

    if user_entry is not None:
        # If an entry for this user already exists, update it
        users.update({key: value}, User.user_id == user_id)
    else:
        # If no entry for this user exists, create a new one
        data = {'user_id': user_id, key: value}
        users.insert(data)

def get_user_data(user_id):
  User = Query()
  return users.search(User.user_id == user_id)[0]

def sanitize(text):
  return re.sub(r'[^\w\s]', '', text)

# Bot commands
@bot.command()
async def set(ctx, key, *, value):

  user_id = str(ctx.author.id)

  value = sanitize(value)

  save_user_data(user_id, key, value)

  await ctx.send(f'Set {key} to {value}')

  # Add a print statement here to output all user data after setting a value
  print(users.all())

@bot.command()
async def novel(ctx):
  user_id = str(ctx.author.id)
  user_data = get_user_data(user_id)

  if 'style' not in user_data or 'genre' not in user_data:
    await ctx.send("Please set both 'style' and 'genre' using the set command before using the novel command.")
    return

  style = user_data['style']
  genre = user_data['genre']

  # Construct the system message to set the behavior of the assistant
  system_message = f"You are an assistant that writes a {genre} story in the style of {style}."

  # Generate the story
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Start the story."}
    ]
  )

  # Extract the assistant's reply
  story = response['choices'][0]['message']['content']

  # Split the story into chunks under the character limit
  chunk_size = 2000  # Discord's character limit for a single message
  story_chunks = [story[i:i+chunk_size] for i in range(0, len(story), chunk_size)]

  # Send each chunk as a separate message
  for chunk in story_chunks:
    await ctx.send(chunk)

  # Send the token cost and USD cost as the last message
  token_cost = response['usage']['total_tokens']
  usd_cost = token_cost * 0.004 / 1000  # Corrected calculation
  await ctx.send(f"Token cost: {token_cost} tokens, USD cost: ${usd_cost:.4f}")  # Adjusted to display four decimal places


@bot.command()
async def hello(ctx):
  await ctx.send("Hello there!")

# Run bot
bot.run(token)
