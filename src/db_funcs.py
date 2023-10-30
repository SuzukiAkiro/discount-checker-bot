import aiosqlite


async def create_user(user_id: int, user_name: str):
    async with aiosqlite.connect("bot.db") as db:
        try:
            await db.execute("""INSERT INTO users VALUES ({id},'{name}')""".format(id=user_id, name=user_name))
        except Exception:
            print('user already exists')
        await db.commit()
