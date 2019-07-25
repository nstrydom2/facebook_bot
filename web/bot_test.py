from unittest import TestCase
from web.bot import Bot

import config.acct_conf as acct
import time

class Bot_TestCase(TestCase):
    def test_login(self):
        bot = Bot()

        try:
            bot.load_fb()
            bot.login(acct.USER, acct.PASS)

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(3)
            bot.close()
