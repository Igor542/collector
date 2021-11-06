import logging

import bot


class Collector:
    def __init__(self):
        # data_base = DB()
        # data_base.open("collector_test")
        # self.backend = TFinance(data_base)
        self.bot = bot.bot()

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
