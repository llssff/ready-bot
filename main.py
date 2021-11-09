# bot.py
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')
fire_emoji = '🔥'
message_map = {}


@bot.command(name='ready')
async def create(ctx, count: int, time=None):
    msg = await ctx.send(count)
    message_map[msg] = set()
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
        print('we dont care about ppl msg')
        return

    #isolate fire emoji amongst reactions
    if reaction.emoji != fire_emoji:
        print("Not fire emoji, do nothing")
        return
    #isolate ppl reactions
    if user.bot:
        print('bot be advanced these days')
        return

    msg = reaction.message
    if msg not in message_map:
        # not tracking this message (already popped or created in prev session)
        return

    # Add user to list
    message_map[msg].add(user)

    param_count = int(msg.content)
    users = message_map[msg]
    if len(users) != param_count:
        return

    channel = msg.channel
    for user in message_map[msg]:
        await user.send("Get In Here!")
    # await channel.send('EveryOne is Ready') # change to dm
    message_map.pop(msg)
    await msg.delete()



bot.run(TOKEN)
