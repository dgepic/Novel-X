import discord
from discord.ext import commands
import openai

# Bot token
token = 'YOUR_DISCORD_BOT_TOKEN'

# OpenAI key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot with intents
bot = commands.Bot(command_prefix='$', intents=intents)

# User preferences
user_data = {}

valid_keys = {'genre', 'style', 'summary', 'world'}

@bot.command()
async def set(ctx, key, *, value):
  user_id = str(ctx.author.id)

  if key not in valid_keys:
    await ctx.send(f'Invalid key. Valid keys are: {valid_keys}')
    return

  if user_id not in user_data:
    user_data[user_id] = {}

  user_data[user_id][key] = value

  await ctx.send(f'Set {key} to {value}')

@bot.command()
async def novel(ctx):
  user_id = str(ctx.author.id)

  if user_id not in user_data or not all(k in user_data[user_id] for k in valid_keys):
    await ctx.send('Please set all preferences before generating a novel.')
    return

  genre = user_data[user_id]['genre']
  style = user_data[user_id]['style']
  summary = user_data[user_id]['summary']
  world = user_data[user_id]['world']

  # Describe the world
  prompt = f"Describe a {world} in a {genre} setting in the style of {style}."
  response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
  world_description = response['choices'][0]['text']

  # Introduce the main characters
  prompt = f"Introduce the main characters of a {genre} novel in the style of {style}. The story takes place in a {world}."
  response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
  character_introduction = response['choices'][0]['text']

  # Write the first chapter
  prompt = f"Write the first chapter of a {genre} novel in the style of {style}. The plot is: {summary}. The story takes place in a {world}."
  response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=300)
  first_chapter = response['choices'][0]['text']

  story = f"{world_description}\n\n{character_introduction}\n\n{first_chapter}"

  await ctx.send(story)

bot.run(token)
