"""
 Starts the polling session via AnimeBot object
"""

import os
import random
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command
import aiohttp
from dotenv import load_dotenv
import requests
from image_search import ImageSearch


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

    command_dict = {"start": "start", "random": "random"}

    def __init__(self, dp) -> None:
        command_dict = {"start": "start", "random": "random"}
        self.dp = dp
        self.command_dict = command_dict
        command_dict = self.command_dict
        self.register_handlers()

    def register_handlers(self):
        """
        register_handlers: standart tuple of the repeatitive commands
        """
        self.dp.register_message_handler(self.start_command,
                                         Command(self.command_dict["start"],
                                                 ignore_case=True))

        self.dp.register_message_handler(self.random_quote,
                                         Command(self.command_dict["random"],
                                                 ignore_case=True))

    @classmethod
    async def start_command(cls, message: types.Message):
        await message.reply(f"こんにちはマスター, this is the list of \
                            avaible commands \
                            {cls.command_dict.keys()}")

    async def image_get(self, query):
        async with aiohttp.ClientSession() as session:
            flickr_api = ImageSearch()
            img_urls = await flickr_api.search_image(session, query)
        return img_urls

    @classmethod
    async def random_quote(self, message: types.Message):
        """
        random_msg Get an response from the random entry point
        of the anime_api service

        response is a simple json object converted into utf-8 text

        Args:
            messge (types.Message): Standart aiogramm class
        """
        random_quote = requests.get("https://animechan.vercel.app/api/random",
                                    timeout=4)
        response = random_quote.json()
        anime = response["anime"]
        character = response["character"]
        quote = response["quote"]
        img_urls = await self.image_get(CommandHandler,
                                        anime + character)
        if len(img_urls) > 0:
            img_url = (random.choice(img_urls))
        else:
            img_url = "https://img.freepik.com/premium-photo/anime-woman-portrait-manga-style-cartoon-illustration_691560-3925.jpg?w=2000"
        await message.answer(f"{anime}\n \
                             {character} \n \
                             {quote} \n")
        await message.reply_photo(photo=img_url)


class MessageHandler:
    """
     Class representing call method
     of the Dispatcher.register_message_handler
    """
    def __init__(self, dp) -> None:
        self.dp = dp
        self.register_handlers()

    def register_handlers(self):
        ...


if __name__ == "__main__":
    load_dotenv(dotenv_path="./token.env")

    TOKEN = "BOT_TOKEN"
    TELEGRAM_TOKEN = os.environ[TOKEN]
    executor.start_polling(AnimeBot(token=TELEGRAM_TOKEN).dp,
                           skip_updates=True)
