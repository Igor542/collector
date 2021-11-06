from telegram.ext import Updater, CommandHandler
from TOKEN import TOKEN

import logging

from backend import respond, tfinance


class bot:
    def __init__(self, backend):
        # Backend to interact with data base
        self.backend = backend
        # Create bot
        self.updater = Updater(token=TOKEN, use_context=True)
        d = self.updater.dispatcher
        # Register API
        d.add_handler(CommandHandler('help', self.help))
        d.add_handler(CommandHandler('register', self.register))
        d.add_handler(CommandHandler('join', self.join))
        d.add_handler(CommandHandler('ack', self.ack))
        d.add_handler(CommandHandler('nack', self.nack))
        d.add_handler(CommandHandler('stat', self.stat))
        d.add_handler(CommandHandler('log', self.log))
        d.add_handler(CommandHandler('payment', self.payment))
        d.add_handler(CommandHandler('g_add', self.g_add))
        d.add_handler(CommandHandler('add', self.add))
        d.add_handler(CommandHandler('cancel', self.cancel))
        d.add_handler(CommandHandler('pay', self.pay))
        d.add_handler(CommandHandler('reset', self.reset))
        # Init internal state
        self.__users = dict()

    def run(self):
        self.updater.start_polling()

    def log_info(func):
        def log(self, update, context):
            logging.info(f'Received command: {update.message.text}')
            return func(self, update, context)
        return log

    def __reply_unimpl(self, update):
        update.message.reply_text('Unimplemented command')

    def __reply_invalid(self, update):
        update.message.reply_text('Invalid command')

    def __reply(self, update, message):
        update.message.reply_text(message)

    def __get_sender_id(self, update):
        return update.message.from_user.id

    def __get_sender_un(self, update):
        return update.message.from_user.username

    def __get_mentioned_ids(self, update):
        msg = update.message
        entities = msg.entities
        mentioned_ids = []

        for e in entities:
            if e.type == 'mention':
                user_begin = e.offset
                user_end = user_begin + e.length
                username = msg.text[user_begin:user_end]
                # TODO: convert username to user_id
                username_id = self.__users.get(username)
                if username_id is None:
                    username_id = -1
                mentioned_ids.append(username_id)
        return mentioned_ids

    # Bot API
    @log_info
    def help(self, update, context):
        # TODO: generate help
        self.__reply_unimpl(update)

    @log_info
    def register(self, update, context):
        sender_id = self.__get_sender_id(update)
        sender_un = self.__get_sender_un(update)
        if self.__users.get(sender_id) is not None:
            # user is already registered
            pass
        else:
            self.__users[sender_id] = sender_un
        # TODO: make a call to Backend with sender_id
        respond = self.backend.register(sender_id)
        if not respond.ok():
            self.__reply(update, respond.error)
        else:
            self.__reply(update, "success")

    @log_info
    def join(self, update, context):
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        if len(mentioned_ids) != 1:
            self.__reply_invalid(update)
    #        self.__reply_help('join')
            return

        # TODO: make a call to Backend with: sender_id, mentioned_ids
        self.__reply_unimpl(update)

    @log_info
    def ack(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        self.__reply_unimpl(update)

    @log_info
    def nack(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        self.__reply_unimpl(update)

    @log_info
    def stat(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        respond = self.backend.stat(sender_id)
        if not respond.ok():
            self.__reply(update, respond.error)
        else:
            self.__reply(update, respond.unpack())

    @log_info
    def log(self, update, context):
        sender_id = self.__get_sender_id(update)
        words = update.message.text.split(' ')
        num_tx = 0
        if len(words) > 1:
            num_tx = int(words[1])
        # TODO: make a call to Backend with: sender_id, num_tx
        self.__reply_unimpl(update)

    @log_info
    def payment(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        self.__reply_unimpl(update)

    @log_info
    def g_add(self, update, context):
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        self.__reply_unimpl(update)

    @log_info
    def add(self, update, context):
        if len(context.args) < 1:
            self.__reply_invalid(update)
            return

        value = context.args[0]
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        respond = self.backend.add(sender_id, float(value), mentioned_ids)
        if not respond.ok():
            self.__reply(update, respond.error)
        else:
            self.__reply(update, "success")

    @log_info
    def cancel(self, update, context):
        sender_id = self.__get_sender_id(update)
        args = context.args
        if len(args) < 1:
            self.__reply_invalid(update)
            return
        tx = args[0]
        comment = ''
        if len(args) > 1:
            comment = args[1]
        # TODO: make a call to Backend with: sender_id, tx, comment
        respond = self.backend.cancel(sender_id, int(tx), comment)
        if not respond.ok():
            self.__reply(update, respond.error)
        else:
            self.__reply(update, "success")

    @log_info
    def pay(self, update, context):
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        self.__reply_unimpl(update)

    @log_info
    def reset(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        self.__reply_unimpl(update)
