import logging

import bot
from backend import db, tfinance


class Collector:
    def __init__(self):
        data_base = db.DB()
        data_base.open("test_db.db")
        backend = tfinance.TFinance(data_base)
        self.bot = bot.bot(backend)

    def run(self):
        self.bot.run()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s'
                        '- %(levelname)s - %(message)s',
                        level=logging.INFO)

    collector = Collector()
    collector.run()


if __name__ == '__main__':
    main()
