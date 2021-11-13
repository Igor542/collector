import logging

from bot_manager import BotManager


class Collector:
    def __init__(self):
        self.bot_manager = BotManager()

    def run(self):
        self.bot_manager.run()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s'
                        '- %(levelname)s - %(message)s',
                        level=logging.INFO)

    collector = Collector()
    collector.run()


if __name__ == '__main__':
    main()
