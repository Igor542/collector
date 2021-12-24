import logging, re
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

    def exit(self):
        logging.info(f'Stopping bot with chat `{self.chat_id}`...')
        self.backend.exit()

    def log_info(func):
        def log(self, update, context):
            logging.info(f'Received command: {update.message.text}')
            logging.info(f'RAW update: {update}')
            try:
                return func(self, update, context)
            except Exception as e:
                logging.error(f'backend failed with exception "{str(e)}"')
                self.__reply(update, f'\U0001F4A9\n"{str(e)}"')
                return None

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
        un = update.message.from_user.username
        if un: return un
        return update.message.from_user.first_name

    def __get_user_id(self, username, sender=None):
        if username == 'me' and sender is not None:
            username = sender
        for key, value in self.__users.items():
            if value == username:
                return key
        return 0

    def __reply_respond(self, update, respond):
        if respond.ok(): return self.__reply(update, "success")
        error = respond.error
        uids = re.findall("%\d+%", error)
        san_uids = ['@' + self.__users[int(uid[1:-1])] for uid in uids]
        for i, s in zip(uids, san_uids):
            error = error.replace(i, s)
        self.__reply(update, error)

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
                username = msg.text[user_begin + 1:user_end]
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
        def usage(update):
            self.__reply(update, 'usage: /register')

        if len(context.args) > 0: return usage(update)

        # register user
        sender_id = int(self.__get_sender_id(update))
        sender_un = self.__get_sender_un(update)
        if self.__users.get(sender_id) is not None:
            # user is already registered
            pass
        else:
            self.__users[sender_id] = sender_un
        respond = self.backend.register(sender_id)
        self.__reply_respond(update, respond)

    @log_info
    def join(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /join @user')

        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        if len(mentioned_ids) != 1: return usage(update)

        respond = self.backend.join(sender_id, mentioned_ids[0])
        self.__reply_respond(update, respond)

    @log_info
    def disjoin(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /disjoin')

        if len(context.args) > 0: return usage(update)

        sender_id = self.__get_sender_id(update)
        respond = self.backend.disjoin(sender_id)
        self.__reply_respond(update, respond)

    @log_info
    def ack(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /ack')

        if len(context.args) > 0: return usage(update)

        sender_id = self.__get_sender_id(update)
        respond = self.backend.ack(sender_id)
        self.__reply_respond(update, respond)

    @log_info
    def nack(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /ack')

        if len(context.args) > 0: return usage(update)

        sender_id = self.__get_sender_id(update)
        respond = self.backend.ack(sender_id)
        self.__reply_respond(update, respond)

    @log_info
    def stat(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /stat')

        if len(context.args) > 0: return usage(update)

        sender_id = self.__get_sender_id(update)
        respond = self.backend.stat(sender_id)
        if not respond.ok():
            return self.__reply(update, respond.error)

        stat_info = respond.unpack()
        reply = ''
        for user_id, value in stat_info.items():
            username = self.__users.get(int(user_id))
            if username is None:
                username = user_id
            reply += f"@{username}: {value:.2f}\n"
        if reply == '':
            reply = 'No data'
        self.__reply(update, reply)

    @log_info
    def log(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /log [@user | me] [num_tx]')

        sender_id = self.__get_sender_id(update)
        words = update.message.text.split(' ')
        if len(words) > 3: return usage(update)

        user_id = None  # default for all users
        num_tx = 10  # default number of transactions
        if len(words) > 2:
            # /log @user | me num_tx
            user_id = self.__get_user_id(words[1])
            if user_id == 0: return usage(update)
            num_tx = int(words[2])
        elif len(words) > 1:
            is_arg_tx = isinstance(words[1], int)
            if is_arg_tx:
                # /log num_tx
                num_tx = int(words[1])
            else:
                # /log @user | me
                user_id = self.__get_user_id(words[1])
                if user_id == 0: return usage(update)

        respond = self.backend.log(sender_id, user_id, num_tx)
        if respond.bad():
            return self.__reply(update, respond.error)

        reply = []
        for r in reversed(respond.unpack()):
            user = ' @' + self.__users.get(int(r.user)) if r.user else ''
            comment = ' ' + r.comment if r.comment else ''
            value = '' if r.value == 0 else f" {r.value:.2f}"
            reply.append(f'({r.tx_id}).{user} {value}  {comment}')
        reply = '\n'.join(reply)
        if not reply:
            reply = 'spend some money first'

        self.__reply(update, reply)

    @log_info
    def payment(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /payment')

        if len(context.args) > 0: return usage(update)

        sender_id = self.__get_sender_id(update)
        respond = self.backend.payment(sender_id)
        if respond.bad():
            return self.__reply(update, respond.error)
        reply = []
        for r in respond.unpack():
            src = '@' + self.__users.get(int(r.src)) if r.src else ''
            dst = '@' + self.__users.get(int(r.dst)) if r.dst else ''
            reply.append(f'{src} -> {dst}: {r.value:.2f}')
        reply = '\n'.join(reply)
        if not reply:
            reply = 'even'

        self.__reply(update, reply)

    @log_info
    def g_add(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /g_add <value> [@user...] [comment]')

        if len(context.args) < 1: return usage(update)

        value = context.args[0]
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        respond = self.backend.g_add(sender_id, float(value), mentioned_ids)
        self.__reply_respond(update, respond)

    @log_info
    def add(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /add <value> [@user...] [comment]')

        if len(context.args) < 1: return usage(update)

        value = context.args[0]
        sender_id = self.__get_sender_id(update)
        mentioned_ids = self.__get_mentioned_ids(update)
        respond = self.backend.add(sender_id, float(value), mentioned_ids)
        self.__reply_respond(update, respond)

    @log_info
    def cancel(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /cancel <tx> [comment]')

        args = context.args
        if len(args) < 1: return usage(update)

        sender_id = self.__get_sender_id(update)
        tx = args[0]
        comment = ''
        if len(args) > 1:
            comment = args[1]
        respond = self.backend.cancel(sender_id, int(tx), comment)
        self.__reply_respond(update, respond)

    @log_info
    def compensate(self, update, context):
        def usage(update):
            self.__reply(update, 'usage: /compensate [comment]')

        args = context.args
        if len(args) > 1: return usage(update)

        sender_id = self.__get_sender_id(update)
        comment = None
        if len(args) == 1:
            comment = arg[0]
        respond = self.backend.compensate(sender_id, comment)
        self.__reply_respond(update, respond)

    @log_info
    def reset(self, update, context):
        sender_id = self.__get_sender_id(update)
        # TODO: make a call to Backend with: sender_id
        self.__reply_unimpl(update)
