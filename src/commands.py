import logging


def log_info(func):
    def log(update, context):
        logging.info(f'Received command: {func}')
        return func(update, context)
    return log


def reply_unimpl(update):
    update.message.reply_text('Unimplemented')


def get_sender_id(update):
    sender = update.message.from_user.id


def get_mentioned_ids(update):
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


@log_info
def help(update, context):
    # TODO: generate help
    reply_unimpl(update)


@log_info
def register(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with sender_id
    reply_unimpl(update)


@log_info
def join(update, context):
    sender_id = get_sender_id(update)
    mentioned_ids = get_mentioned_ids(update)
    assert(len(mentioned_ids) == 1)
    # TODO: make a call to Backend with: sender_id, mentioned_ids
    reply_unimpl(update)


@log_info
def ack(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with: sender_id
    reply_unimpl(update)


@log_info
def nack(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with: sender_id
    reply_unimpl(update)


@log_info
def stat(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with: sender_id
    reply_unimpl(update)


@log_info
def log(update, context):
    sender_id = get_sender_id(update)
    words = update.message.text.split(' ')
    print(words)
    num_tx = 0
    if len(words) > 1:
        num_tx = int(words[1])
    # TODO: make a call to Backend with: sender_id, num_tx
    reply_unimpl(update)


@log_info
def payment(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with: sender_id
    reply_unimpl(update)


@log_info
def g_add(update, context):
    sender_id = get_sender_id(update)
    mentioned_ids = get_mentioned_ids(update)
    # TODO: make a call to Backend with: sender_id, mentioned_ids
    reply_unimpl(update)


@log_info
def add(update, context):
    sender_id = get_sender_id(update)
    mentioned_ids = get_mentioned_ids(update)
    # TODO: make a call to Backend with: sender_id, mentioned_ids
    reply_unimpl(update)


@log_info
def cancel(update, context):
    sender_id = get_sender_id(update)
    words = update.message.text.split(' ')
    assert(len(words) >= 2)
    tx = words[1]
    comment = ''
    if len(words) > 2:
        comment = words[2]
    # TODO: make a call to Backend with: sender_id, tx, comment
    reply_unimpl(update)


@log_info
def pay(update, context):
    sender_id = get_sender_id(update)
    mentioned_ids = get_mentioned_ids(update)
    # TODO: make a call to Backend with: sender_id, mentioned_ids
    reply_unimpl(update)


@log_info
def reset(update, context):
    sender_id = get_sender_id(update)
    # TODO: make a call to Backend with: sender_id
    reply_unimpl(update)
