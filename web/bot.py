import schedule

from logging import getLogger
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

from config import proxy as proxy_conf
from config import acct_conf
from config import bot_conf
from web.bot_utils import BotUtils


class Bot(BotUtils):
    def __init__(self, logging=None, proxy=False, headless=False):
        super(Bot, self).__init__()
        self.bot_logger = getLogger()

        if logging is not None or len(logging) != 0:
            for level in logging:
                if level is 'INFO':
                    self.bot_logger.setLevel(logging.INFO)
                if level is 'ERROR':
                    self.bot_logger.setLevel(logging.ERROR)
                if level is 'DEBUG':
                    self.bot_logger.setLevel(logging.DEBUG)

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

        options = webdriver.FireFoxOptions()

        if headless is True:
            options.add_argument('--headless')

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
            self.bot_logger.info('Browser driver has been initialized')

    def bot_startup(self):
        self.parse_bot_config()
        self.load_scheduler()

    def parse_bot_config(self):
        try:
            self.bot_logger.info('Parsing bot config file')

            if len(bot_conf.PROGRAMMER) is not 0:
                raise Exception("Could not load bot config!")

            for directive, value in bot_conf.PROGRAMMER.items():
                if directive.lower() is "random likes per month":
                    self.likes_monthly = value
                    self.bot_logger.debug('Random likes per month has been set')

                elif directive.lower() is "like specifc post tags per month":
                    self.tags_list = value
                    self.bot_logger.debug('Specific post tags have been set')

                elif directive.lower() is "send group request":
                    self.groups_list = value
                    self.bot_logger.debug('Group request flag has been set')

                elif directive.lower() is "random videos per month":
                    self.like_vids_monthly = value
                    self.bot_logger.debug('Videos per month have been set')

                elif directive.lower() is "accept all friend requests":
                    self.accept_all_requests = value.lower() is "yes"
                    self.bot_logger.debug('Accept all friend requests flag has been set')

                elif directive.lower() is "send friend requests":
                    self.send_requests = value.lower is "yes"
                    self.bot_logger.debug('Send friend requests flag has been set')

                elif directive.lower() is "random images post per month":
                    self.post_imgs = value
                    self.bot_logger.debug('Randoms images posted per month has been set')

                else:
                    raise Exception("Invalid directive!")

        except Exception as ex:
            self.bot_logger.error('Error --> ' + ex)

    def load_scheduler(self):
        try:
            self.bot_logger.info('Loading scheduler')

            ##
            ## ! Don't forget to edit this section !
            ##
            if self.likes_monthly > 0:
                schedule.every(2).day.at("10:30").do(self.random_like())
                self.bot_logger.debug('Scheduled random likes')

            # if self.tags_list is not None:
            #     schedule.every(2).day.at("10:30").do(self.random_like())
            #     self.bot_logger.debug('Scheduled ')
            #
            # if self.groups_list is not None:
            #     schedule.every(2).day.at("10:30").do(self.random_like())

            if self.like_vids_monthly > 0:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())
                self.bot_logger.debug('Scheduled liked videos')

            if self.accept_all_requests is True:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())
                self.bot_logger.debug('Scheduled accepting requests')

            if self.send_requests is True:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())
                self.bot_logger.debug('Scheduled sending friend requets')

            if self.post_imgs > 0:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())
                self.bot_logger.debug('Scheduled posting images')

        except Exception as ex:
            self.bot_logger.error('Error --> ' + ex)

    def like_all_feed_posts(self, num_posts=50):
        next_button = '/html/body/div/div/div[2]/div/div[4]/a'

        for num in range(1, num_posts):
            self.like_post(num)
            self.wait()

            if num % 8 == 0:
                self.driver.find_element_by_xpath(next_button).click()
                self.wait()

    def accept_all_friend_requests(self, max=50):
        for index in range(max):
            self.accept_friend_request(index)

