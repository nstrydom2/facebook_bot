import schedule
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options

from config import proxy as proxy_conf
from config import acct_conf
from config import bot_conf
from web.bot_utils import BotUtils


bot_logger = logging.getLogger('facebook_bot.web.bot')

class Bot():
    def __init__(self, logger=None, proxy=False, headless=False):
        self.logger = logger
        self.setup_log()

        geckdriver_path = r'/home/ghost/Drivers/geckodriver'

        # Initialize class variables
        self.fb_url = 'https://mbasic.facebook.com/'

        # Bot directive variables
        self.likes_monthly = 0
        self.tags_list = None
        self.groups_list = None
        self.like_vids_monthly = 0
        self.accept_all_requests = False
        self.send_requests = True
        self.post_imgs = 0

        browser_profile = webdriver.FirefoxProfile()
        browser_profile.set_preference('dom.webnotifications.enabled', False)

        options = Options()
        options.headless = headless

        # Prob create selenium instance here
        if proxy_conf.LIST is None:
            self.driver = webdriver.Firefox(executable_path=geckdriver_path,
                                            firefox_profile=browser_profile,
                                            firefox_options=options)
            self.bot_logger.info('Browser driver has been initialized')
        else:
            # Set up proxy if 'proxy' variables' value is True
            proxy_server = Proxy()
            proxy_server.proxy_type = ProxyType.MANUAL
            proxy_server.http_proxy = proxy_conf.LIST['http']
            proxy_server.socks_proxy = proxy_conf.LIST['sock']
            proxy_server.ssl_proxy = proxy_conf.LIST['ssl']

            capabilities = webdriver.DesiredCapabilities.FIREFOX
            proxy_server.add_to_capabilities(capabilities)

            self.driver = webdriver.Firefox(executable_path=geckdriver_path,
                                            firefox_profile=browser_profile,
                                            desired_capabilities=capabilities)
            bot_logger.info('Browser driver has been initialized')

        self.bot_utils = BotUtils(self.driver, self.fb_url)

    def setup_log(self):
        stream_handler = logging.StreamHandler()

        if self.logger is not None:
            for level in self.logger:
                if level is 'INFO':
                    stream_handler.setLevel(logging.INFO)
                if level is 'DEBUG':
                    stream_handler.setLevel(logging.DEBUG)
        stream_handler.setLevel(logging.ERROR)

        # Set logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)

        # Apply handler to log
        bot_logger.addHandler(stream_handler)

    def bot_startup(self):
        bot_logger.info('Bot is starting...')
        self.parse_bot_config()
        self.bot_utils.load_fb()
        self.bot_utils.login()
        self.load_scheduler()

        while True:
            schedule.run_pending()
            time.sleep(1)


    def parse_bot_config(self):
        try:
            bot_logger.info('Parsing bot config file')

            if len(bot_conf.PROGRAMMER) == 0:
                raise Exception("Could not load bot config!")

            for directive, value in bot_conf.PROGRAMMER.items():
                if directive.lower() is "random likes per month":
                    self.likes_monthly = value
                    bot_logger.debug('Random likes per month has been set')

                elif directive.lower() is "like specific post tags per month":
                    self.tags_list = value
                    bot_logger.debug('Specific post tags have been set')

                elif directive.lower() is "send group request":
                    self.groups_list = value
                    bot_logger.debug('Group request flag has been set')

                elif directive.lower() is "random videos per month":
                    self.like_vids_monthly = value
                    bot_logger.debug('Videos per month have been set')

                elif directive.lower() is "accept all friend requests":
                    self.accept_all_requests = value.lower() is "yes"
                    bot_logger.debug('Accept all friend requests flag has been set')

                elif directive.lower() is "send friend requests":
                    self.send_requests = value.lower is "yes"
                    bot_logger.debug('Send friend requests flag has been set')

                elif directive.lower() is "random images post per month":
                    self.post_imgs = value
                    bot_logger.debug('Randoms images posted per month has been set')

                else:
                    raise Exception("Invalid directive -- " + directive)

        except Exception as ex:
            bot_logger.error(str(ex))

    def load_scheduler(self):
        try:
            bot_logger.info('Loading scheduler')

            ##
            ## ! Don't forget to edit this section !
            ##
            if self.likes_monthly > 0:
                schedule.every(1).days.at("10:30").do(self.bot_utils.random_like)
                bot_logger.debug('Scheduled random likes')

            # if self.tags_list is not None:
            #     schedule.every(2).day.at("10:30").do(self.random_like())
            #     self.bot_logger.debug('Scheduled ')
            #
            # if self.groups_list is not None:
            #     schedule.every(2).day.at("10:30").do(self.random_like())

            if self.like_vids_monthly > 0:
                schedule.every(1).days.at("10:30").do(self.bot_utils.random_like)
                bot_logger.debug('Scheduled liked videos')

            if self.accept_all_requests is True:
                schedule.every(1).days.at("10:30").do(self.accept_all_friend_requests)
                bot_logger.debug('Scheduled accepting requests')

            if self.send_requests is True:
                schedule.every(1).days.at("10:30").do(self.bot_utils.add_all_recommended)
                bot_logger.debug('Scheduled sending friend requests')

            if self.post_imgs > 0:
                schedule.every(1).days.at("10:30").do(self.bot_utils.upload_picture)
                bot_logger.debug('Scheduled posting images')

        except Exception as ex:
            bot_logger.error(str(ex))

    def like_all_feed_posts(self, num_posts=50):
        next_button = '/html/body/div/div/div[2]/div/div[4]/a'

        for num in range(1, num_posts):
            self.bot_utils.like_post(num)
            self.bot_utils.wait()

            if num % 8 == 0:
                self.driver.find_element_by_xpath(next_button).click()
                self.bot_utils.wait()

    def accept_all_friend_requests(self, max=50):
        for index in range(max):
            self.bot_utils.accept_friend_request(index)

