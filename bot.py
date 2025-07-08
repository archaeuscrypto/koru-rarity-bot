import discord
from discord.ext import commands
import json
import os

with open('rarity-ranking.json') as f:
    rarity_data = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def rarity(ctx, token_number: int):
    token_str = str(token_number)
    if token_str in rarity_data:
        data = rarity_data[token_str]
        await ctx.send(
            f'#{token_number} → Tier: **{data["tier"]}** | Rank: **{data["rank"]}** | '
            f'Percentile: **{data["percentile"]}%** | Score: `{data["score"]}`'
        )
    else:
        await ctx.send(f'No rarity data found for #{token_number}.')

bot.run(os.getenv("DISCORD_TOKEN"))