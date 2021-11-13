import logging

from backend import respond, tfinance


class Bot:
    def __init__(self, bot, chat_id, backend):
        self.bot = bot
        self.chat_id = chat_id
        self.backend = backend
        # Add users
        self.__users = dict()
        respond = backend.db.get_all_users()
        if respond.ok():
            user_ids = respond.unpack()
            for uid in user_ids:
                member = bot.get_chat_member(user_id=uid, chat_id=chat_id)
                username = member.user.username
                if username is None:
                    username = member.user.first_name
                self.__users[int(uid)] = username

    def log_info(func):
        def log(self, update, context):
            logging.info(f'Received command: {update.message.text}')
            logging.info(f'RAW update: {update}')
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

    def __get_user_id(self, username):
        for key, value in self.__users.items():
            if value == username:
                return key
        return 0

    def __get_mentioned_ids(self, update):
        msg = update.message
        entities = msg.entities
        mentioned_ids = []

        for e in entities:
            if e.type == 'text_mention':
                user_id = e.user.id
                mentioned_ids.append(user_id)
            if e.type == 'mention':
                user_begin = e.offset
                user_end = user_begin + e.length
                username = msg.text[user_begin:user_end]
                # TODO: convert username to user_id
                user_id = self.__get_user_id(username)
                if user_id is None:
                    user_id = -1
                mentioned_ids.append(user_id)
        return mentioned_ids

    # Bot API
    @log_info
    def help(self, update, context):
        # TODO: generate help
        self.__reply_unimpl(update)

    @log_info
    def register(self, update, context):
        # register user
        sender_id = int(self.__get_sender_id(update))
        sender_un = self.__get_sender_un(update)
        if self.__users.get(sender_id) is not None:
            # user is already registered
            pass
        else:
            self.__users[sender_id] = sender_un
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
            stat_info = respond.unpack()
            reply = ''
            for user_id, value in stat_info.items():
                username = self.__users.get(int(user_id))
                if username is None:
                    username = user_id
                reply += f"@{username}: {value}\n"
            self.__reply(update, reply)

    @log_info
    def log(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /log [@user | me] [num_tx]')

        sender_id = self.__get_sender_id(update)
        words = update.message.text.split(' ')
        if len(words) > 3: return usage(update)

        user_id = None # default for all users
        num_tx = 10    # default number of transactions
        if len(words) > 2:
            num_tx = int(words[2])
            if words[1].startswith('@'):
                user_id = self.__get_mentioned_ids(update)[0]
            elif words[1] == 'me':
                user_id = sender_id
            else:
                return usage(update)

        respond = self.backend.log(sender_id, user_id, num_tx)
        if respond.bad():
            self.__reply(update, respond.error)
            return

        reply = []
        for r in repond.unpack():
            user = self.__users.get(int(r.user))
            reply.append(f'({r.tx_id}). @{user}  {r.value}  {r.comment}')
        reply = '\n'.join(reply)

        self.__reply(update, reply)

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
