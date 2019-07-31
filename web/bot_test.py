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

    def test_load_facebook(self):
        bot = Bot()

        try:
            bot.load_fb()

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(3)
            bot.close()

    def test_load_friend_requests(self):
        bot = Bot()

        try:
            bot.load_fb()
            bot.login(acct.USER, acct.PASS)
            bot.load_friends_requests()

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(3)
            bot.close()

    def test_load_wall(self):
        bot = Bot()

        try:
            bot.load_fb()
            bot.login(acct.USER, acct.PASS)
            bot.load_wall()

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(3)
            bot.close()

    def test_upload_pic(self):
        bot = Bot()

        try:
            bot.load_fb()
            bot.login(acct.USER, acct.PASS)

            # Upload method
            bot.upload_picture(caption='Test upload', img_path='pictures/profile_pic.jpg')

        except Exception as ex:
            print(ex)

        finally:
            time.sleep(3)
            bot.close()
