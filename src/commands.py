import logging


def log_info(func):
    def log(update, context):
        logging.info(f'Received command: {func}')
        return func(update, context)
    return log

def reply_unimpl(update):
    update.message.reply_text('Unimplemented')

@log_info
def help(update, context):
    reply_unimpl(update)


@log_info
def register(update, context):
    reply_unimpl(update)


@log_info
def join(update, context):
    reply_unimpl(update)


@log_info
def ack(update, context):
    reply_unimpl(update)


@log_info
def nack(update, context):
    reply_unimpl(update)


@log_info
def stat(update, context):
    reply_unimpl(update)


@log_info
def log(update, context):
    reply_unimpl(update)


@log_info
def payment(update, context):
    reply_unimpl(update)


@log_info
def g_add(update, context):
    reply_unimpl(update)


@log_info
def add(update, context):
    reply_unimpl(update)


@log_info
def cancel(update, context):
    reply_unimpl(update)


@log_info
def pay(update, context):
    reply_unimpl(update)


@log_info
def reset(update, context):
    reply_unimpl(update)
