import discord
from discord.ext import commands
import random
import asyncio
import json
import os
import time

# 유저 돈 저장용 딕셔너리
user_money = {}

# 슬롯에 사용할 이모지
slots = ["🍒", "🍋", "🔔", "💎", "7️⃣"]


intents = discord.Intents.all()
intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
client = discord.Client(intents=intents)

client = commands.Bot(command_prefix="!", intents=intents)

@client.event 
async def on_ready():
    print("ready")
    bar = discord.Game("봇 작업중...")
    await client.change_presence(status=discord.Status.online, activity=bar)
    
@client.command(aliases=['로그인', '접속하기기'])
async def login(ctx):
    await ctx.send("{} | {}님, 어서오세요!".format(ctx.author, ctx.author.mention))

@client.command(aliases=['야', '개미'])
async def 개미야(ctx):
    await ctx.send("왜")
 
@client.command()
async def 도배(ctx):
    await ctx.send("도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배도배")
 

@client.command(aliases=['임베드'])
async def 설명(interaction: discord.Interaction):
    
    embed = discord.Embed(title='개미봇')
    embed.add_field(name="제작자", value="개미")
    embed.add_field(name="제작자", value="개미")
 

    await interaction.send(embed=embed)


@client.command(name='유저정보')
async def get_user_info(ctx, *, user_input: str = None):
    if not user_input:
        await ctx.send("사용자 이름 또는 멘션을 입력해주세요. 예: `!유저정보 @유저` 또는 `!유저정보 닉네임`")
        return

    # 멘션된 유저가 있다면 그 유저를 사용
    if ctx.message.mentions:
        user = ctx.message.mentions[0]
    else:
        # 서버에서 닉네임 또는 이름으로 유저 검색
        user = discord.utils.find(lambda m: m.name == user_input or m.display_name == user_input, ctx.guild.members)

    if not user:
        await ctx.send("해당 유저를 찾을 수 없습니다.")
        return

    embed = discord.Embed(title="유저 정보", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="ID", value=f"{user.name}#{user.discriminator}", inline=False)
    embed.add_field(name="이름", value=user.display_name, inline=False)
    # embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="계정 생성일", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="서버 가입일", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S') if user.joined_at else "N/A", inline=False)

    await ctx.send(embed=embed)



JACKPOT_FILE = "jack.json"




MONEY_FILE = "money.json"

# 슬롯 이모지
ANIMATION_ICONS = ["🍒", "🍋", "🔔", "💎", "7️⃣"]  # 🎰 제외
RESULT_ICONS = ["🍒", "🍋", "🔔", "💎", "7️⃣", "🎰"]  # 🎰 포함

# 배당률
PAYOUTS = {
    "🍒": 2,
    "🍋": 4,
    "🔔": 5,
    "💎": 7,
    "7️⃣": 10,
    "🎰": None  # 🎰은 잭팟
}

# 확률 설정 (백분율 기준)
PROBABILITIES = {
    "🍒": 10.0,
    "🍋": 7.0,
    "🔔": 4.0,
    "💎": 0.5,
    "7️⃣": 0.1,
    "🎰": 0.01
}

# 돈 저장/로드
def load_money():
    if os.path.exists(MONEY_FILE):
        with open(MONEY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_money():
    with open(MONEY_FILE, "w", encoding="utf-8") as f:
        json.dump(user_money, f, indent=4, ensure_ascii=False)

user_money = load_money()
jackpot = 0  # 잭팟 변수

# 돈줘
last_give_time = {}

# 💾 돈 저장/로드
def load_money():
    if os.path.exists(MONEY_FILE):
        with open(MONEY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_money():
    with open(MONEY_FILE, "w", encoding="utf-8") as f:
        json.dump(user_money, f, indent=4, ensure_ascii=False)

user_money = load_money()


def load_jack():
    if os.path.exists(JACKPOT_FILE):
        with open(JACKPOT_FILE, "r", encoding="utf-8") as f:
            return int(f.read())
    return 0

def save_jack():
    with open(JACKPOT_FILE, "w", encoding="utf-8") as f:
        f.write(str(jackpot))

jackpot = load_jack()


# 💸 !돈줘 명령어 (랜덤 지급 + 1분 쿨타임)
@client.command(name='돈줘')
async def give_money(ctx):
    user_id = str(ctx.author.id)
    now = time.time()

    # 쿨타임 체크
    if user_id in last_give_time and now - last_give_time[user_id] < 60:
        remaining = int(60 - (now - last_give_time[user_id]))
        await ctx.send(f"⏱️ {ctx.author.mention}님, 돈은 1분마다 받을 수 있어요! 남은 시간: {remaining}초")
        return

    # 랜덤 금액 지급
    amount = random.randint(1000, 10000)
    user_money[user_id] = user_money.get(user_id, 0) + amount
    last_give_time[user_id] = now
    save_money()

    await ctx.send(f"💸 {ctx.author.mention}님에게 {amount}원이 지급되었습니다! (1분 후에 다시 받을 수 있어요)")

# 돈 확인
@client.command(name='돈')
async def check_money(ctx):
    user_id = str(ctx.author.id)
    money = user_money.get(user_id, 0)
    await ctx.send(f"{ctx.author.mention}님의 현재 잔액은 {money}원입니다.")

# 잭팟 확인
@client.command(name='잭팟')
async def check_jackpot(ctx):
    await ctx.send(f"🎰 현재 잭팟에 모인 돈은 {jackpot}원입니다.")


# 슬롯머신
@client.command(name='슬롯머신')
async def slot_machine(ctx, amount: int):
    global jackpot
    user_id = str(ctx.author.id)
    money = user_money.get(user_id, 0)


    if amount <= 0:
        await ctx.send("❗ 돈액수는 1000 이상이어야 합니다.")
        return

    if money < amount:
        await ctx.send(f"❌ {ctx.author.mention}님의 잔액이 부족합니다. 현재 잔액: {money}원")
        return

# ❗ 최소 금액 제한
    if amount < 1000:
        await ctx.send(f"❗ 최소 배팅 금액은 1000원입니다. {ctx.author.mention}")
        return

    if money < amount:
        await ctx.send(f"❌ {ctx.author.mention}님의 잔액이 부족합니다. 현재 잔액: {money}원")
        return

    # 💸 돈 차감 및 잭팟 적립
    user_money[user_id] = money - amount
    jackpot += amount
    save_money()
    save_jack()  # ⬅️ 저장 추가

    msg = await ctx.send("🎰 슬롯머신 작동 중...")

    # 1초 애니메이션 (🎰 제외)
    for _ in range(3):
        temp = [random.choice(ANIMATION_ICONS) for _ in range(3)]
        await msg.edit(content=f"🎰 {' | '.join(temp)}")
        await asyncio.sleep(1 / 3)

    # 확률 기반 결과 생성
    result = generate_weighted_result()
    await msg.edit(content=f"🎰 {' | '.join(result)}")

    if result.count(result[0]) == 3:
        symbol = result[0]
        if symbol == "🎰":
            reward = jackpot
            user_money[user_id] += reward
            await ctx.send(f"🎰🎉 {ctx.author.mention}님! 🎰🎰🎰 잭팟 당첨! {reward}원을 획득했습니다!")
            jackpot = 0  # 잭팟 초기화
            save_jack()  # ⬅️ 잭팟 초기화 저장
        else:
            payout = PAYOUTS.get(symbol, 0)
            reward = amount * payout
            user_money[user_id] += reward
            await ctx.send(f"🎉 {ctx.author.mention}님! {symbol*3} 당첨! {payout}배로 {reward}원을 획득했습니다!")
        save_money()
    else:
        await ctx.send(f"😢 아쉽네요, {ctx.author.mention}! 다시 도전해보세요.")

# 확률 기반 결과 생성 함수
def generate_weighted_result():
    """동일한 이모지 3개가 나올 확률에 따라 전체 결과를 결정"""
    roll = random.uniform(0, 100)
    cumulative = 0.0

    for symbol, chance in PROBABILITIES.items():
        cumulative += chance
        if roll <= cumulative:
            return [symbol] * 3

    # 당첨 안 되면 랜덤으로 다른 조합
    return [random.choice(RESULT_ICONS) for _ in range(3)]


access_token == os.environ["BOT_TOKEN"]
client.run(access_token)
