from telegram.ext import Updater, CommandHandler
from TOKEN import TOKEN

import logging


class bot:
    def __init__(self, backend):
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

    def __get_sender_id(update):
        sender = update.message.from_user.id

    def __get_mentioned_ids(update):
        msg = update.message
        entities = msg.entities
        mentioned_ids = []

        for e in entities:
            if e.type == 'mention':
                user_begin = e.offset
                user_end = user_begin + e.length
                username = msg.text[user_begin:user_end]
                # TODO: convert username to user_id
                username_id = username
                mentioned_ids.append(username_id)
        return mentioned_ids

    # Bot API
    @log_info
    def help(self, update, context):
        # TODO: generate help
        self.__reply_unimpl(update)

    @log_info
    def register(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with sender_id
        __reply_unimpl(update)

    @log_info
    def join(self, update, context):
        sender_id = __get_sender_id(update)
        mentioned_ids = __get_mentioned_ids(update)
        if len(mentioned_ids) != 1:
            __reply_invalid(update)
    #        __reply_help('join')
            return

        # TODO: make a call to Backend with: sender_id, mentioned_ids
        __reply_unimpl(update)

    @log_info
    def ack(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        __reply_unimpl(update)

    @log_info
    def nack(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        __reply_unimpl(update)

    @log_info
    def stat(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        __reply_unimpl(update)

    @log_info
    def log(self, update, context):
        sender_id = __get_sender_id(update)
        words = update.message.text.split(' ')
        print(words)
        num_tx = 0
        if len(words) > 1:
            num_tx = int(words[1])
        # TODO: make a call to Backend with: sender_id, num_tx
        __reply_unimpl(update)

    @log_info
    def payment(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        __reply_unimpl(update)

    @log_info
    def g_add(self, update, context):
        sender_id = __get_sender_id(update)
        mentioned_ids = __get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        __reply_unimpl(update)

    @log_info
    def add(self, update, context):
        sender_id = __get_sender_id(update)
        mentioned_ids = __get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        __reply_unimpl(update)

    @log_info
    def cancel(self, update, context):
        sender_id = __get_sender_id(update)
        words = update.message.text.split(' ')
        if len(words) < 2:
            __reply_invalid(update)
            return
        tx = words[1]
        comment = ''
        if len(words) > 2:
            comment = words[2]
        # TODO: make a call to Backend with: sender_id, tx, comment
        __reply_unimpl(update)

    @log_info
    def pay(self, update, context):
        sender_id = __get_sender_id(update)
        mentioned_ids = __get_mentioned_ids(update)
        # TODO: make a call to Backend with: sender_id, mentioned_ids
        __reply_unimpl(update)

    @log_info
    def reset(self, update, context):
        sender_id = __get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        __reply_unimpl(update)
