import schedule

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

from config import proxy as proxy_conf
from config import acct_conf
from config import bot_conf
from web.bot_utils import BotUtils


class Bot(BotUtils):
    def __init__(self, proxy=False):
        super(Bot, self).__init__()

        browser_profile = webdriver.FirefoxProfile()
        browser_profile.set_preference('dom.webnotifications.enabled', False)

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

        # Prob create selenium instance here
        if proxy_conf.LIST is None:
            self.driver = webdriver.Firefox(executable_path=geckdriver_path,
                                            firefox_profile=browser_profile)
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

    def bot_startup(self):
        self.parse_bot_config()
        self.load_scheduler()

    def parse_bot_config(self):
        try:
            if len(bot_conf.PROGRAMMER) is not 0:
                raise Exception("Could not load bot config!")

            for directive, value in bot_conf.PROGRAMMER.items():
                if directive.lower() is "random likes per month":
                    self.likes_monthly = value

                elif directive.lower() is "random videos per month":
                    self.like_vids_monthly = value

                elif directive.lower() is "accept all friend requests":
                    self.accept_all_requests = value.lower() is "yes"

                elif directive.lower() is "send friend requests":
                    self.send_requests = value.lower is "yes"

                elif directive.lower() is "random images post per month":
                    self.post_imgs = value

                elif directive.lower() is "like specifc post tags per month":
                    self.post_imgs = value

                elif directive.lower() is "send group request":
                    self.post_imgs = value

                elif directive.lower() is "random images post per month":
                    self.post_imgs = value

                else:
                    raise Exception("Invalid directive!")

        except Exception as ex:
            print(ex)

    def load_scheduler(self):
        try:
            ##
            ## ! Don't forget to edit this section !
            ##
            if self.likes_monthly > 0:
                schedule.every(2).day.at("10:30").do(self.random_like())

            if self.like_vids_monthly > 0:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())

            if self.accept_all_requests is True:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())

            if self.send_requests is True:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())

            if self.post_imgs > 0:
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())

        except Exception as ex:
            pass

    def like_all_feed_posts(self, num_posts=50):
        next_button = '/html/body/div/div/div[2]/div/div[4]/a'

        for num in range(1, num_posts):
            self.like_post(num)
            self.wait()

            if num % 8 == 0:
                self.driver.find_element_by_xpath(next_button).click()
                self.wait()

    def add_all_recommended(self, limit=150):
        self.load_friends_requests()

        try:
            for friend in range(1, limit):
                # Click on 'Add Friend' button of recommended friend
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/form/div/div/div[1]/ul[1]/li[' +
                    str(friend) + ']/div/div/div/div[2]/div[2]/div/div/div/div/div/button[1]'
                ).click()
                self.wait()

        except:
            pass

    def accept_all_friend_requests(self, max=50):
        self.driver
        self.load_friends_requests()

        for index in range(max):
            self.accept_friend_request(index)

