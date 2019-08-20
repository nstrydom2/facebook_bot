import argparse

from web import bot


parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help='enable verbose mode')

parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='enable debug mode')

parser.add_argument('-p', '--proxy',
                    action='store_true',
                    help='enable proxy')

args = parser.parse_args()
logging = []
proxy = args.p

if args.v is True:
    logging.append('INFO')
if args.d is True:
    logging.append('DEBUG')

fb_bot = bot.Bot(logging=logging, proxy=proxy)
fb_bot.bot_startup()