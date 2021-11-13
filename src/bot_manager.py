import os

from telegram.ext import Updater, CommandHandler
from TOKEN import TOKEN

import bot
from backend import db, tfinance


class BotManager:
    def __init__(self):
        # Load existing chats
        # - Create a bot for each chat

        # Create Telegram bot
        self.updater = Updater(token=TOKEN, use_context=True)
        # Register API
        commands = [
            'help', 'register', 'join', 'ack', 'nack', 'stat', 'log',
            'payment', 'g_add', 'add', 'cancel', 'pay', 'reset'
        ]
        for c in commands:
            self.__register_command(c)
        self.__bots = dict()
        # init data directory
        self.cur_dir = os.getcwd()
        self.data_dir = self.cur_dir + '/__data'
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)

    def run(self):
        self.updater.start_polling()

    def __get_chat_id(self, update):
        return update.message.chat.id

    def __get_bot(self, chat_id):
        b = self.__bots.get(chat_id)
        if b is None:
            # try to find existing db
            chat_dir = self.data_dir + '/' + str(chat_id)
            if not os.path.isdir(chat_dir):
                os.mkdir(chat_dir)
            # Create a new bot
            data_base = db.DB()
            data_base.open(f"{chat_dir}/db.db")
            backend = tfinance.TFinance(data_base)
            b = bot.Bot(backend)
            self.__bots[chat_id] = b
        return b

    def __redirect2bot(self, update, context):
        chat_id = self.__get_chat_id(update)
        bot = self.__get_bot(chat_id)
        command = update.message.text.split(' ')[0][1:]
        return bot.__getattribute__(command)(update, context)

    def __register_command(self, name):
        # Register in Telegram Bot
        self.updater.dispatcher.add_handler(
            CommandHandler(name, self.__redirect2bot))
