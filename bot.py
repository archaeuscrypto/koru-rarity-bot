import discord
from discord.ext import commands
import json
import os

# Add allowed user IDs here (as integers)
ALLOWED_USER_IDS = {1031627979975049308, 768910258570919947}  # Replace with actual user IDs

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
intents.message_content = True  # Required to read message content
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands')
    except Exception as e:
        print(f'Error syncing commands: {e}')

# Add this event handler
@bot.event
async def on_message(message: discord.Message):
    # Ignore messages from bots
    if message.author.bot:
        return
    # Allow slash commands or messages from allowed users
    if message.content.startswith("/") or message.author.id in ALLOWED_USER_IDS:
        await bot.process_commands(message)
        return
    try:
        await message.delete()
    except discord.Forbidden:
        pass  # Bot lacks permission to delete
    except discord.HTTPException:
        pass  # Message already deleted or other error

# /info command
@bot.tree.command(name="info", description="Show all available bot commands")
async def info(interaction: discord.Interaction):
    message = (
        "**Available Commands:**\n"
        "• `/rarity <number>` → Check rarity of a specific NFT\n"
        "• `/top` → Show top 25 rarest NFTs\n"
        "• `/stats` → Show total supply per rarity tier\n"
        "• `/info` → Show this list of commands"
    )
    await interaction.response.send_message(message, ephemeral=True)

# /stats command
@bot.tree.command(name="stats", description="Show total supply of NFTs per tier")
async def stats(interaction: discord.Interaction):
    tier_counts = {tier: 0 for tier in tier_emojis.keys()}

    for data in rarity_data.values():
        tier = data["tier"]
        if tier in tier_counts:
            tier_counts[tier] += 1

    message_lines = ["**NFT Supply per Tier** 📊"]
    for tier, count in tier_counts.items():
        emoji = tier_emojis.get(tier, "")
        message_lines.append(f"{emoji} **{tier}**: {count}")

    total = len(rarity_data)
    message_lines.append(f"\n**Total NFTs:** {total}")

    await interaction.response.send_message("\n".join(message_lines), ephemeral=True)

# /rarity command
@bot.tree.command(name="rarity", description="Check rarity of a token by number")
async def rarity(interaction: discord.Interaction, nft_number: int):
    token_str = str(nft_number)
    if token_str in rarity_data:
        data = rarity_data[token_str]
        emoji = tier_emojis.get(data["tier"], "")
        message = (
            f"**NFT #{nft_number}**\n"
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
@bot.tree.command(name="top", description="Show the top 25 rarest nfts")
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
            f"NFT #{token_id} → {emoji} **{data['tier']}** | Rank: **{data['rank']}** | Percentile: **{data['percentile']}%**"
        )

    await interaction.response.send_message("\n".join(message_lines), ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))
