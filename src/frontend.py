from telegram.ext import Updater, CommandHandler
from TOKEN import TOKEN

import logging
import commands


def init_bot():
    # Create bot
    updater = Updater(token=TOKEN, use_context=True)
    d = updater.dispatcher

    # Register API
    d.add_handler(CommandHandler('help', commands.help))
    d.add_handler(CommandHandler('register', commands.register))
    d.add_handler(CommandHandler('join', commands.join))
    d.add_handler(CommandHandler('ack', commands.ack))
    d.add_handler(CommandHandler('nack', commands.nack))
    d.add_handler(CommandHandler('stat', commands.stat))
    d.add_handler(CommandHandler('log', commands.log))
    d.add_handler(CommandHandler('payment', commands.payment))
    d.add_handler(CommandHandler('g_add', commands.g_add))
    d.add_handler(CommandHandler('add', commands.add))
    d.add_handler(CommandHandler('cancel', commands.cancel))
    d.add_handler(CommandHandler('pay', commands.pay))
    d.add_handler(CommandHandler('reset', commands.reset))

    # Run bot
    updater.start_polling()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s'
                        '- %(levelname)s - %(message)s',
                        level=logging.INFO)

    # TODO: Connect to Backend

    # Init bot
    init_bot()


if __name__ == '__main__':
    main()
