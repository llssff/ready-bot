# bot.py
import os
import re
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')
fire_emoji = '🔥'
message_map = {}


@bot.command(name='ready')
async def create(ctx, count: int, content="chilling"):

    #retard check
    if count == 1:
        await ctx.message.delete()
        return

    msg = await ctx.send(f'{count} attendees\nPurpose: {content}')
    message_map[msg] = {ctx.message.author}
    await msg.add_reaction(fire_emoji)
    await ctx.message.delete()


@bot.command(name='clear')
async def clear(ctx):
    for msg in message_map:
        await msg.delete()
    message_map.clear()
    await ctx.message.delete()


@bot.event
async def on_reaction_add(reaction, user):
    #isolate bot messages
    if reaction.message.author != bot.user:
        return

    #isolate fire emoji amongst reactions
    if reaction.emoji != fire_emoji:
        return

    #isolate ppl reactions
    if user.bot:
        return

    msg = reaction.message

    # not tracking this message (already popped or created in prev session)
    if msg not in message_map:
        return

    # Add user to list
    message_map[msg].add(user)
    param_count = int(re.search(r'\d+', msg.content).group(0))
    users = message_map[msg]
    if len(users) != param_count:
        return

    # channel = msg.channel
    param_purpose = "\n".join(msg.content.split("\n")[1:])
    for user in message_map[msg]:
        await user.send(f"You've been summoned for:\n{param_purpose}")

    message_map.pop(msg)
    await msg.delete()

bot.run(TOKEN)
