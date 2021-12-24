import os
import re
import logging

import telegram
from telegram.ext import Updater, CommandHandler

import bot
from backend import db, tfinance


class BotManager:
    def __init__(self, token_file, data_dir):
        # Load existing chats
        # - Create a bot for each chat

        # Create Telegram bot
        self.bot = telegram.Bot(token=self.__read_token(token_file))
        self.updater = Updater(bot=self.bot,
                               use_context=True,
                               user_sig_handler=self.exit)
        # Register API
        COMMANDS = [
            'help', 'register', 'join', 'disjoin', 'ack', 'nack', 'stat',
            'log', 'payment', 'g_add', 'add', 'cancel', 'compensate'
        ]
        for c in COMMANDS:
            self.__register_command(c)
        self.__bots = dict()
        # init data directory
        self.data_dir = data_dir
        if not os.path.isdir(self.data_dir):
            os.mkdir(self.data_dir)

    def __read_token(self, token_file):
        def complain(s):
            logging.critical(f'{s}. Exiting...')
            exit(2)

        if not os.path.isfile(token_file):
            complain(f'Token file "{token_file}" is not found')
        with open(token_file, 'r') as f:
            token = f.readlines()

        if len(token) != 1:
            complain(
                f'Token file should have exactly one line (now has {len(token)})'
            )
        token = token[0].strip()

        if not re.match(r'^\d+:\w+$', token):
            complain(f'Token has wrong format')
        return token

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def exit(self, signo, stack_frame):
        logging.info(f'Stopping bot_manager...')
        self.updater.stop()
        for _, bot in self.__bots.items():
            bot.exit()

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
            b = bot.Bot(self.bot, chat_id, backend)
            self.__bots[chat_id] = b
        return b

    def __redirect2bot(self, update, context):
        chat_id = self.__get_chat_id(update)
        bot = self.__get_bot(chat_id)
        command = update.message.text.split(' ')[0][1:]
        return bot.__getattribute__(command)(update, context)

    def __register_command(self, name):
        if getattr(bot.Bot, name, None) is not None:
            self.updater.dispatcher.add_handler(
                CommandHandler(name, self.__redirect2bot))
