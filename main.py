import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import time

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

answers = [
    "是",
    "否",
    "理論上可以",
    "數據上偏向不行",
    "你其實已經知道答案了",
    "這問題本身就很危險",
    "看心情",
    "問我幹嘛?",
    "隨便",
    "嗯",
    "你他媽有病是不是?",
    "我覺得你應該去檢查一下智商",
    "從邏輯上來說，是",
    "理性判斷，不太可能",
    "依條件而定",
    "不是",
    "也許",
    "絕對是",
    "絕對不是",
    "你真的覺得這是個好問題嗎？",
    "你要不要冷靜一下再問",
    "這問題有點浪費空氣",
    "你要不要聽聽看你在說甚麼?",
    "你他媽有病是不是?",
    "啟智",
    ":)?",
    "問之前動一下腦子",
    "晚餐兒",
    "隨便啦",
    "我懶得想",
    "你開心就好",
    ": )",
    "...",
    "問題本身就是答案",
    "你確定你在找答案嗎？",
    "也許沒有正確解",
    "🤡",
    "笑死",
    "握草",
    "喔",
    "幹",
    "Get out!!!!!"

]

emojis = ["😂", "😈", "🤔", "💀", "🙃", "👀"]

follow_questions = [
    "那你自己怎麼想？",
    "你是希望我說是還是否？",
    "如果真的發生了你會怎麼辦？",
    "你敢照這個答案做嗎？",
    "你其實比較想聽哪個？",
    "你是想被支持，還是想被打醒？",
    "你敢照這個答案做嗎？",
    "如果你不服，問題也不在我",
    "你可以不認同，但我的答案不會改",
    "給我擦皮鞋"
]

idle_questions = [
    "為甚麼1+1=3？",
    "有人其實已經有答案了吧？",
    "如果重來一次，你會選不一樣的嗎？",
    "成功跟快樂哪個比較重要？",
    "義大利麵是否要辦42號混提土？"
]

lonely_lines = [
    "好喔，看來沒人想回答",
    "這題太難了是不是",
    "bro你們是啞巴嗎?",
]

recent_users = []
last_message_time = time.time()
last_idle_question_time = 0

@bot.event
async def on_ready():
    idle_loop.start()
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    global last_message_time

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    last_message_time = time.time()

    if message.author.id not in recent_users:
        recent_users.append(message.author.id)
        if len(recent_users) > 10:
            recent_users.pop(0)

    content = message.content.strip()

    if not content.endswith(("?", "？")):
        return

    reply = random.choice(answers)
    if random.random() < 0.35:
        reply += " " + random.choice(emojis)

    await message.reply(reply)

    if random.random() < 0.25:
        await asyncio.sleep(random.uniform(0.6, 1.2))
        q = random.choice(follow_questions)
        if random.random() < 0.4:
            q += " " + random.choice(emojis)
        await message.channel.send(q)

@tasks.loop(seconds=120)
async def idle_loop():
    global last_idle_question_time

    now = time.time()

    if now - last_message_time < 600:
        return

    if now - last_idle_question_time < 1800:
        return

    if random.random() > 0.35:
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    if recent_users and random.random() < 0.4:
        user_id = random.choice(recent_users)
        mention = f"<@{user_id}> "
    else:
        mention = ""

    q = mention + random.choice(idle_questions)
    if random.random() < 0.4:
        q += " " + random.choice(emojis)

    await channel.send(q)
    last_idle_question_time = now

    await asyncio.sleep(60)
    if time.time() - last_message_time > 660:
        await channel.send(random.choice(lonely_lines))

bot.run(TOKEN)
