#! /usr/bin/env python3
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

parser.add_argument('-H', '--headless',
                    action='store_true',
                    help='run the bot in headless mode')

args = parser.parse_args()
logger = []
proxy = args.proxy
headless = args.headless

if args.verbose is True:
    logger.append('INFO')
#if args.debug is True:
logger.append('DEBUG')

fb_bot = bot.Bot(logger=logger, proxy=proxy, headless=headless)
fb_bot.bot_startup()

