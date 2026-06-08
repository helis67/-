import asyncio
import os
import aiosqlite

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
Message,
InlineKeyboardMarkup,
InlineKeyboardButton,
CallbackQuery
)
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

bot = Bot(TOKEN)
dp = Dispatcher()

DB_NAME = "mafia.db"

# ---------------- DATABASE ----------------

async def create_db():
async with aiosqlite.connect(DB_NAME) as db:
await db.execute("""
CREATE TABLE IF NOT EXISTS users(
telegram_id INTEGER PRIMARY KEY,
username TEXT,
diamonds INTEGER DEFAULT 0,
games INTEGER DEFAULT 0,
wins INTEGER DEFAULT 0,
vip INTEGER DEFAULT 0
)
""")
await db.commit()

async def add_user(user_id, username):
async with aiosqlite.connect(DB_NAME) as db:
await db.execute(
"""
INSERT OR IGNORE INTO users
(telegram_id, username)
VALUES (?, ?)
""",
(user_id, username)
)
await db.commit()

async def get_user(user_id):
async with aiosqlite.connect(DB_NAME) as db:
cursor = await db.execute(
"""
SELECT *
FROM users
WHERE telegram_id = ?
""",
(user_id,)
)

```
    return await cursor.fetchone()
```

async def add_diamonds(user_id, amount):
async with aiosqlite.connect(DB_NAME) as db:
await db.execute(
"""
UPDATE users
SET diamonds = diamonds + ?
WHERE telegram_id = ?
""",
(amount, user_id)
)
await db.commit()

async def remove_diamonds(user_id, amount):
async with aiosqlite.connect(DB_NAME) as db:
await db.execute(
"""
UPDATE users
SET diamonds = diamonds - ?
WHERE telegram_id = ?
""",
(amount, user_id)
)
await db.commit()

async def activate_vip(user_id):
async with aiosqlite.connect(DB_NAME) as db:
await db.execute(
"""
UPDATE users
SET vip = 1
WHERE telegram_id = ?
""",
(user_id,)
)
await db.commit()

# ---------------- START ----------------

@dp.message(Command("start"))
async def start_cmd(message: Message):
username = message.from_user.username

```
if username:
    username = f"@{username}"
else:
    username = message.from_user.full_name

await add_user(
    message.from_user.id,
    username
)

await message.answer(
    "🎭 Добро пожаловать в Mafia Bot\n\n"
    "/profile - профиль\n"
    "/shop - магазин"
)
```

# ---------------- PROFILE ----------------

@dp.message(Command("profile"))
async def profile(message: Message):
user = await get_user(
message.from_user.id
)

```
if not user:
    return

vip = "👑 Да" if user[5] else "❌ Нет"

await message.answer(
    f"👤 {user[1]}\n\n"
    f"💎 Алмазы: {user[2]}\n"
    f"🎮 Игр: {user[3]}\n"
    f"🏆 Побед: {user[4]}\n"
    f"{vip}"
)
```

# ---------------- SHOP ----------------

@dp.message(Command("shop"))
async def shop(message: Message):
kb = InlineKeyboardMarkup(
inline_keyboard=[
[
InlineKeyboardButton(
text="👑 VIP - 500💎",
callback_data="buy_vip"
)
]
]
)

```
await message.answer(
    "🛒 Магазин",
    reply_markup=kb
)
```

@dp.callback_query(F.data == "buy_vip")
async def buy_vip(callback: CallbackQuery):
user = await get_user(
callback.from_user.id
)

```
diamonds = user[2]

if diamonds < 500:
    await callback.answer(
        "Недостаточно алмазов",
        show_alert=True
    )
    return

await remove_diamonds(
    callback.from_user.id,
    500
)

await activate_vip(
    callback.from_user.id
)

await callback.message.answer(
    "👑 VIP успешно куплен"
)

await callback.answer()
```

# ---------------- ADMIN ----------------

@dp.message(Command("give"))
async def give(message: Message):
username = message.from_user.username

```
if username != ADMIN_USERNAME:
    return

args = message.text.split()

if len(args) != 3:
    await message.answer(
        "/give ID АЛМАЗЫ"
    )
    return

user_id = int(args[1])
amount = int(args[2])

await add_diamonds(
    user_id,
    amount
)

await message.answer(
    "Готово"
)
```

# ---------------- RUN ----------------

async def main():
await create_db()
await dp.start_polling(bot)

if **name** == "**main**":
asyncio.run(main())

