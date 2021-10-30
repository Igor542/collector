from telegram.ext import Updater, CommandHandler
from TOKEN import TOKEN

import logging
import commands

def init_bot():
    # Create bot
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register API
    dispatcher.add_handler(CommandHandler('help', commands.help))

    # Run bot
    updater.start_polling()

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    init_bot()

if __name__ == '__main__':
    main()
