import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("DISCORD_TOKEN")
WORK_CHANNEL_ID = 1466808167831830681

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"已上線：{bot.user}")

def analyze(is_video):
    score = random.randint(40, 85)

    pros = [
        "至少你有剪，不是原片直接丟",
        "畫面沒有爛到讓人想直接關掉",
        "內容有想法，不是完全亂拍",
        "至少不是低能作品"
    ]

    cons_pool = [
        "bro 你這剪輯節奏慢到我以為在等公車",
        "bro 你背景音樂跟畫面是在各做各的事嗎",
        "bro 你這構圖是隨便拍還是手機掉地上",
        "bro 你這轉場真的很敢用",
        "bro 你鏡頭亂晃，是在拍地震紀錄片嗎",
        "bro 我朋友看了還以為是測試檔",
        "bro 說真的，我阿嬤剪的都比較順",
        "bro 你這色調是在考驗觀眾眼睛嗎"
    ]

    advice = [
        "前五秒直接重點，不然真的留不住人",
        "剪輯節奏拉快一點，別怕刪",
        "背景音樂音量壓低，別跟人聲打架",
        "拍之前先想好你要表達什麼",
        "多看幾個熱門作品學結構"
    ]

    pros_text = random.choice(pros)
    cons_text = "、".join(random.sample(cons_pool, 3))
    advice_text = random.choice(advice)

    return score, pros_text, cons_text, advice_text

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != WORK_CHANNEL_ID:
        return

    if not message.attachments:
        return

    attachment = message.attachments[0]
    content_type = attachment.content_type or ""
    is_video = "video" in content_type

    score, pros, cons, advice = analyze(is_video)

    reply = (
        f"🎯 作品評分：{score}/100\n\n"
        f"優點：{pros}\n\n"
        f"缺點（超毒舌）：{cons}\n\n"
        f"建議：{advice}"
    )

    await message.reply(reply)
    await bot.process_commands(message)

bot.run(TOKEN)

