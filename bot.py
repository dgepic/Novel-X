
async def send_large_message(ctx, text):
    for i in range(0, len(text), 2000):
        await ctx.send(text[i:i+2000])


# A dictionary to store user data
user_data_store = {}

# A function to get user data
def get_user_data(user_id):
    # Get the data for the user, or return an empty dictionary if the user doesn't exist
    return user_data_store.get(user_id, {})

# A function to set user data
def set_user_data(user_id, user_data):
    # Set the data for the user
    user_data_store[user_id] = user_data


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

@bot.command()
async def BrainX(ctx, *, brainx: str):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)
    user_data['BrainX'] = brainx
    set_user_data(user_id, user_data)
    await ctx.send(f"BrainX set to: {brainx}")

@bot.command()
async def Genre(ctx, *, genre: str):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)
    user_data['Genre'] = genre
    set_user_data(user_id, user_data)
    await ctx.send(f"Genre set to: {genre}")

@bot.command()
async def Style(ctx, *, style: str):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)
    user_data['Style'] = style
    set_user_data(user_id, user_data)
    await ctx.send(f"Style set to: {style}")

@bot.command()
async def GenerateSynopsis(ctx):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)

    # Construct the system message to set the behavior of the assistant
    system_message = f"You are an assistant that generates a synopsis based on the following information: BrainX: {user_data['BrainX']}, Genre: {user_data['Genre']}, Style: {user_data['Style']}."

    # Generate the synopsis
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Generate a synopsis."}
        ]
    )

    # Extract the assistant's reply
    synopsis = response['choices'][0]['message']['content']

    # Store the synopsis
    user_data['Synopsis'] = synopsis
    set_user_data(user_id, user_data)

    # Send the synopsis as a message
    await send_large_message(ctx, synopsis)

@bot.command()
async def GenerateChapterOutline(ctx):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)

    # Construct the system message to set the behavior of the assistant
    system_message = f"You are an assistant that generates a chapter outline based on the following information: BrainX: {user_data['BrainX']}, Genre: {user_data['Genre']}, Style: {user_data['Style']}, Synopsis: {user_data['Synopsis']}."

    # Generate the chapter outline
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Generate a chapter outline."}
        ]
    )

    # Extract the assistant's reply
    chapter_outline = response['choices'][0]['message']['content']

    # Store the chapter outline
    user_data['ChapterOutline'] = chapter_outline
    set_user_data(user_id, user_data)

    # Send the chapter outline as a message
    await send_large_message(ctx, chapter_outline)

@bot.command()
async def GenerateChapterBeats(ctx):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)

    # Construct the system message to set the behavior of the assistant
    system_message = f"You are an assistant that generates chapter beats based on the following information: BrainX: {user_data['BrainX']}, Genre: {user_data['Genre']}, Style: {user_data['Style']}, Synopsis: {user_data['Synopsis']}, Chapter Outline: {user_data['ChapterOutline']}."

    # Generate the chapter beats
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Generate chapter beats."}
        ]
    )

    # Extract the assistant's reply
    chapter_beats = response['choices'][0]['message']['content']

    # Store the chapter beats
    user_data['ChapterBeats'] = chapter_beats
    set_user_data(user_id, user_data)

    # Send the chapter beats as a message
    await send_large_message(ctx, chapter_beats)

@bot.command()
async def GenerateChapter(ctx):
    user_id = str(ctx.author.id)
    user_data = get_user_data(user_id)

    # Construct the system message to set the behavior of the assistant
    system_message = f"You are an assistant that generates a chapter based on the following information: BrainX: {user_data['BrainX']}, Genre: {user_data['Genre']}, Style: {user_data['Style']}, Synopsis: {user_data['Synopsis']}, Chapter Outline: {user_data['ChapterOutline']}, Chapter Beats: {user_data['ChapterBeats']}."

    # Generate the chapter
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Generate a chapter."}
        ]
    )

    # Extract the assistant's reply
    chapter = response['choices'][0]['message']['content']

    # Send the chapter as a message
    await send_large_message(ctx, chapter)

# Run bot
bot.run(token)
