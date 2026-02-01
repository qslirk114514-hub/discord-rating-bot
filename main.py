import discord
from discord.ext import commands
import random
import asyncio
import os

TOKEN = os.environ["TOKEN"]
REVIEW_CHANNEL_ID = int(os.environ["REVIEW_CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def analyze(is_video):
    score = random.randint(35, 95)

    if is_video:
        pros = [
            "至少你有剪，不是原片直接丟",
            "畫面沒晃到讓人想吐，算你贏",
            "內容有一點點想法",
            "不是完全腦腐，勉強給過",
            "有在試著說故事"
        ]

        cons_pool = [
            "bro 你這剪輯節奏慢到我以為影片卡住",
            "bro 你開頭爛到觀眾三秒內直接滑走",
            "bro 你背景音樂吵成這樣是在趕人嗎",
            "bro 你轉場用得很敢，但真的很醜",
            "bro 你鏡頭切這麼亂是在測試觀眾耐心",
            "bro 你影片一半都是廢片段",
            "bro 你構圖像事故現場",
            "bro 我阿嬤剪得都比你順"
        ]

        advice = [
            "前五秒不丟重點，觀眾根本不欠你",
            "剪掉廢片段，你會感覺影片突然變好看",
            "背景音樂壓低，不要跟內容打架",
            "拍之前先想好，不然只是在亂錄"
        ]
    else:
        pros = [
            "主體至少拍得到",
            "色調沒爆掉，眼睛還活著",
            "構圖有稍微想過",
            "畫面不至於災難"
        ]

        cons_pool = [
            "bro 你背景亂到主體直接消失",
            "bro 你亮度怪到像螢幕壞掉",
            "bro 你構圖歪成這樣不是藝術",
            "bro 你這角度真的很迷",
            "bro 你照片沒重點，看了不知道在拍什麼",
            "bro 你這張很像隨手拍完就放生",
            "bro 你是不是沒檢查就直接傳了"
        ]

        advice = [
            "背景簡化，不然照片永遠很亂",
            "亮度跟對比先救一下眼睛",
            "多拍幾張再選，不要一張定生死",
            "裁切一下，讓主體站出來"
        ]

    selected_cons = random.sample(cons_pool, k=3)

    toxic_finishers = [
        "不是針對你，是作品真的站不住腳",
        "如果你不服，問題也不在我",
        "我只是分析，受傷是你自己的事",
        "你可以不認同，但分數不會改",
        "下次會不會比較好，我不敢保證"
    ]

    return score, random.choice(pros), selected_cons, random.choice(advice), random.choice(toxic_finishers)

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != REVIEW_CHANNEL_ID:
        return

    if not message.attachments:
        return

    file = message.attachments[0].filename.lower()

    is_image = file.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    is_video = file.endswith((".mp4", ".mov", ".avi", ".webm"))

    if not (is_image or is_video):
        await message.reply("我只評圖片跟影片，其他我真的懶得看")
        return

    await message.channel.send("☠️ bro 等一下，我正在組織語言準備嘴你")
    await asyncio.sleep(2)

    score, pro, cons_list, advice, finisher = analyze(is_video)

    embed = discord.Embed(
        title="🔥 超毒舌評審結果",
        color=discord.Color.dark_red()
    )

    embed.add_field(name="📊 分數", value=f"{score} / 100", inline=False)
    embed.add_field(name="✅ 勉強能看的地方", value=pro, inline=False)
    embed.add_field(name="💀 缺點（嘴到你懷疑人生）", value="\n".join(cons_list), inline=False)
    embed.add_field(name="🧠 如果你真的想變好", value=advice, inline=False)
    embed.set_footer(text=finisher)

    await message.reply(embed=embed)

bot.run(TOKEN)
