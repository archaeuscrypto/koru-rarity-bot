import discord
from discord.ext import commands
import json
import os

with open('rarity-ranking.json') as f:
    rarity_data = json.load(f)

# Tier → Emoji mapping
tier_emojis = {
    "Mythic": "🟣",
    "Legendary": "🟡",
    "Epic": "🟢",
    "Rare": "🔵",
    "Common": "⚪"
}

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

# /rarity command
@bot.tree.command(name="rarity", description="Check rarity of a token by number")
async def rarity(interaction: discord.Interaction, nft_number: int):
    token_str = str(nft_number)
    if token_str in rarity_data:
        data = rarity_data[token_str]
        emoji = tier_emojis.get(data["tier"], "")
        message = (
            f"**#{nft_number}**\n"
            f"Tier: {emoji} **{data['tier']}**\n"
            f"Rank: **{data['rank']}**\n"
            f"Percentile: **{data['percentile']}%**"
        )
        await interaction.response.send_message(message, ephemeral=True)
    else:
        await interaction.response.send_message(
            f"No rarity data found for #{nft_number}.", ephemeral=True
        )

# /top command
@bot.tree.command(name="top", description="Show the top 5 rarest tokens")
async def top(interaction: discord.Interaction):
    # Sort tokens by rank ascending
    sorted_tokens = sorted(
        rarity_data.items(),
        key=lambda item: item[1]["rank"]
    )[:25]

    message_lines = ["**Top 25 Rarest NFTs** 🔥"]
    for token_id, data in sorted_tokens:
        emoji = tier_emojis.get(data["tier"], "")
        message_lines.append(
            f"#{token_id} → {emoji} **{data['tier']}** | Rank: **{data['rank']}** | Percentile: **{data['percentile']}%**"
        )

    await interaction.response.send_message("\n".join(message_lines), ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
