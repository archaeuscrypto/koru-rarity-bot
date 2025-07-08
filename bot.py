import discord
from discord.ext import commands
import json
import os

with open('rarity-ranking.json') as f:
    rarity_data = json.load(f)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

# Slash command version of /rarity
@bot.tree.command(name="rarity", description="Check rarity of a token by number")
async def rarity(interaction: discord.Interaction, token_number: int):
    token_str = str(token_number)
    if token_str in rarity_data:
        data = rarity_data[token_str]
        await interaction.response.send_message(
            f'#{token_number} → Tier: **{data["tier"]}** | Rank: **{data["rank"]}** | '
            f'Percentile: **{data["percentile"]}%** | Score: `{data["score"]}`',
            ephemeral=True  # 👈 This makes it visible ONLY to the user
        )
    else:
        await interaction.response.send_message(
            f'No rarity data found for #{token_number}.',
            ephemeral=True
        )

bot.run(os.getenv("DISCORD_TOKEN"))
