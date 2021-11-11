# bot.py
import os
import re
from dotenv import load_dotenv
from discord import *
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=".")
slash = SlashCommand(client, sync_commands=True)

guild_ids = [171029138226806785]

fire_emoji = '🔥'
message_map = {}


@slash.slash(
    name='ready',
    guild_ids=guild_ids,
)
async def _ready(ctx: SlashContext, count: int, content: str = "chilling"):
    #retard check
    if count == 1:
        await ctx.message.delete()
        return

    msg = await ctx.send(f'{count} attendees\nPurpose: {content}')
    message_map[msg] = {ctx.author}
    await msg.add_reaction(fire_emoji)


@client.event
async def on_raw_reaction_remove(payload):
    # step 1: find the message
    msg = find_message(payload.message_id)

    # could not find the message
    if not msg:
        return

    # step 2: find the user in that list
    user = find_user(payload.user_id, msg)

    # somehow couldn't find user in list of reactions saved (author?)
    if not user:
        return

    # step 3: delete them
    message_map[msg].remove(user)


@client.event
async def on_reaction_add(reaction, user):
    #isolate bot messages
    if reaction.message.author != client.user:
        return

    #isolate fire emoji amongst reactions
    if reaction.emoji != fire_emoji:
        return

    #isolate ppl reactions
    if user.bot:
        return

    #find message by id in message_map(msg:reaction_author)
    #_ready stored SlashMessage where as reaction.message is of type Message
    msg = find_message(reaction.message.id)

    if not msg:
        return

    # Add user to list
    message_map[msg].add(user)
    param_count = int(re.search(r'\d+', msg.content).group(0))
    users = message_map[msg]
    if len(users) != param_count:
        return

    param_purpose = "\n".join(msg.content.split("\n")[1:])
    map(lambda u: await u.send(f"You've been summoned for:\n{param_purpose}"), message_map[msg])

    message_map.pop(msg)
    await msg.delete()

def find_message(message_id: int):
    return next(filter(lambda m: m.id == message_id, message_map), None)

def find_user(user_id: int, msg):
    return next(filter(lambda u: u.id == user_id, message_map[msg]), None)


client.run(TOKEN)
