import asyncio, logging, sys
from os import getenv

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from sqlalchemy import BIGINT, insert, select, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session

BOT_TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher(storage=MemoryStorage())

load_dotenv()
Base = declarative_base()
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
DB_CONFIG = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DB_CONFIG)
session = Session(engine)


class User(Base):
    __tablename__ = "bot_users"
    id: Mapped[int] = mapped_column(__type_pos=BIGINT, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(__type_pos=BIGINT)
    fullname: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(nullable=True)

    def insert(self, user_id, fullname, username):
        user_data = {
            "user_id": user_id,
            "fullname": fullname,
            "username": username,
        }
        user: User | None = session.execute(select(User).where(User.user_id == user_id)).fetchone()
        if not user:
            query = insert(User).values(**user_data)
            session.execute(query)
            session.commit()

    def select(self):
        users_datas = session.execute(select(User.user_id, User.fullname, User.username)).fetchall()
        return users_datas


Base.metadata.create_all(engine)


@dp.message(CommandStart())
async def start_handler(msg: Message, state: FSMContext):
    User.insert(Base,msg.from_user.id, msg.from_user.full_name, msg.from_user.username)
    await msg.answer(f"Hello - 👤 {msg.from_user.full_name}")
    print(f"👤 - {msg.from_user.full_name}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
