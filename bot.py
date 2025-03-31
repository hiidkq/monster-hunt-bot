import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="/", intents=intents)

# Load monster data
monsters = {
    "Young Potbelly": "<:YoungPotbelly:1355921268263878898>",
    "Young Mammott": "<:YoungMammott:1355921388262654123>",
    "Young Tweedle": "<:YoungTweedle:1355921462803959897>",
    "Young Toe Jammer": "<:YoungToeJammer:1355921536703397992>",
    "Young Noggin": "<:YoungNoggin:1355921659818676274>"
}

# In-memory storage for user hunts and completions
user_hunts = {}
user_completions = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.slash_command(name="hunt")
async def hunt(ctx, monster: str):
    if monster not in monsters:
        await ctx.send(f"{monster} is not a valid monster. Please choose a valid monster.", ephemeral=True)
        return
    
    user_id = ctx.author.id
    user_hunts[user_id] = monster
    await ctx.send(f"You have started hunting for {monster}. Good luck!", ephemeral=True)

@bot.slash_command(name="hunt-end")
async def hunt_end(ctx):
    user_id = ctx.author.id
    if user_id not in user_hunts:
        await ctx.send("You are not currently hunting any monster.", ephemeral=True)
        return
    
    monster = user_hunts.pop(user_id)
    if user_id not in user_completions:
        user_completions[user_id] = []
    
    user_completions[user_id].append(monster)
    await ctx.send(f"Congratulations! You have successfully hunted {monster} and it has been added to your collection.", ephemeral=True)

@bot.slash_command(name="monster-completion")
async def monster_completion(ctx, user: discord.User = None):
    user = user or ctx.author
    user_id = user.id
    completions = user_completions.get(user_id, [])
    
    embed = discord.Embed(title=f"{user.name}'s Monster Completion")
    for monster, emoji in monsters.items():
        collected = "✅" if monster in completions else "❌"
        embed.add_field(name=f"{emoji} {monster}", value=collected, inline=True)
    
    await ctx.send(embed=embed)

bot.run('YOUR_BOT_TOKEN')
