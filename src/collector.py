import argparse
import logging

from bot_manager import BotManager


class Collector:
    def __init__(self, token_file, data_dir):
        self.bot_manager = BotManager(token_file, data_dir)

    def run(self):
        self.bot_manager.run()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Telegram bot to track money spendings')
    parser.add_argument('-t',
                        '--token',
                        type=str,
                        default='__data/secrets/TOKEN',
                        help='path to telegram bot token file')
    parser.add_argument('-d',
                        '--data',
                        type=str,
                        default='__data/storage',
                        help='path for data storage directory')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()

    LOG_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = LOG_LEVELS[min(args.verbose, len(LOG_LEVELS) - 1)]

    logging.basicConfig(format='%(asctime)s - %(name)s'
                        '- %(levelname)s - %(message)s',
                        level=logging.INFO)

    collector = Collector(args.token, args.data)
    collector.run()


if __name__ == '__main__':
    main()
