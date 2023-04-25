"""
 Starts the polling session via AnimeBot object
"""

import os
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import requests


class AnimeBot:
    """
     Represents a bot object with the quick definition
     of the Bot interface, Dispatcher
    """
    def __init__(self, token) -> None:
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)
        self.command_handler = CommandHandler(self.dp)
        self.message_handler = MessageHandler(self.dp)


class CommandHandler:
    """
     Command handler that executes during polling session

    Accepts dp object (Aiogram.Dispatcher class)
    """
    def __init__(self, dp) -> None:
        self.dp = dp
        self.register_handlers()

    def register_handlers(self):
        """
        register_handlers: standart tuple of the repeatitive commands
        """
        self.dp.register_message_handler(self.start_command,
                                         commands=["start"])

    async def start_command(self, message: types.Message):
        await message.reply("こんにちはマスター")


class MessageHandler:
    """
     Class representing call method
     of the Dispatcher.register_message_handler
    """
    def __init__(self, dp) -> None:
        self.dp = dp
        self.register_handlers()

    def register_handlers(self):
        self.dp.register_message_handler(self.random_msg)

    async def random_msg(self, messge: types.Message):
        """
        random_msg Get an response from the random entry point
        of the anime_api service

        response is a simple json object converted into utf-8 text

        Args:
            messge (types.Message): Standart aiogramm class
        """
        random_quote = requests.get("https://animechan.vercel.app/api/random",
                                    timeout=4)
        response = random_quote.text
        await messge.answer(response)


if __name__ == "__main__":
    load_dotenv(dotenv_path="./token.env")

    TOKEN = "BOT_TOKEN"
    TELEGRAM_TOKEN = os.environ[TOKEN]
    executor.start_polling(AnimeBot(token=TELEGRAM_TOKEN).dp,
                           skip_updates=True)
