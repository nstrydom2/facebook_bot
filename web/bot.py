import schedule

from random import randrange

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

from config import proxy as proxy_conf
from config import acct_conf
from config import bot_conf


class Bot():
    def __init__(self, proxy=False):
        browser_profile = webdriver.FirefoxProfile()
        browser_profile.set_preference('dom.webnotifications.enabled', False)

        geckdriver_path = r'/home/ghost/Drivers/geckodriver'

        # Prob create selenium instance here
        if proxy is False:
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
        # Initialize class variables
        self.fb_url = 'https://mbasic.facebook.com/'

        # Bot directive variables
        self.likes_monthly = 0
        self.like_vids_monthly = 0
        self.accept_all_requests = False
        self.send_requests = True
        self.post_imgs = 0

    def start(self):
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
                schedule.every(2).day.at("10:30").do(self.like_feed_posts())

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

    def load_fb(self):
        self.driver.get(self.fb_url)
        self.wait()

    def load_wall(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/h1/a/span').click()
        self.wait()

    def load_profile(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a'
        ).click()
        self.wait()

    # Login to facebook
    def login(self, usr, passwd):
        email_element = self.driver.find_element_by_name('email')
        pass_element = self.driver.find_element_by_name('pass')

        email_element.send_keys(usr)
        pass_element.send_keys(passwd)

        self.driver.find_element_by_name('login').click()
        self.wait()

        self.driver.find_element_by_xpath('/html/body/div/div/div/div/table/tbody/tr/td/div/div[3]/a').click()
        self.wait()

    def load_friends_requests(self):
        friends_button_xpath = '/html/body/div/div/div[1]/div/div/a[6]'
        friend_requests_xpath = '/html/body/div/div/div[2]/div/div[1]/div[1]/a'

        # Click friend requests button
        self.driver.find_element_by_xpath(friends_button_xpath).click()
        self.wait()

        # Click 'See All' in friend requests drop down
        self.driver.find_element_by_xpath(friend_requests_xpath).click()
        self.wait()

    def like_feed_posts(self, num_posts=50):
        next_button = '/html/body/div/div/div[2]/div/div[4]/a'

        for num in range(1, num_posts):
            xpath = '/html/body/div/div/div[2]/div/div[4]/div[3]/div[{0}]/div[2]/div[2]/span[1]/a[1]'.format(num)

            try:
                self.driver.find_element_by_xpath(xpath).click()
                self.wait()

                if num % 8 == 0:
                    self.driver.find_element_by_xpath(next_button).click()
                    self.wait()

            except:
                pass

    def add_recommended(self, limit=150):
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


    def accept_all_friend_requests(self):
        self.load_friends_requests()
        pass

    def upload_picture(self, caption='', img_path=''):
        upload_button_xpath = '/html/body/div/div/div[2]/div/div[2]/div/form/div[2]/span/div[1]/table/tbody/tr/td[2]/input'
        file_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/form/div[1]/div/input[1]'
        preview_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/form/div[3]/input[1]'
        post_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/div/form/input[19]'

        # self.driver.find_element_by_xpath(
        #     '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div' +
        #     '/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/ul/li[1]/div/div/span/a'
        # ).click()

        # Click Upload Photo link/button
        self.driver.find_elements_by_xpath(upload_button_xpath)[0].click()
        self.wait()

        # Select Pic to upload
        self.driver.find_element_by_xpath(file_button_xpath)[0].click()
        self.wait()

        # Click Preview button
        self.driver.find_element_by_xpath(preview_button_xpath)[0].click()
        self.wait()

        # Click Post button
        self.driver.find_element_by_xpath(post_button_xpath)[0].click()

        # file_upload = self.driver.find_element_by_xpath('//*[@id="js_5g2"]')
        # file_upload.send_keys(img_path)
        #
        # status_text_in = self.driver.find_element_by_xpath(
        #     '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div/div[2]/div[1]' +
        #     '/div/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/div/div/div/div/div/div/div'
        # )
        # status_text_in.send_keys(caption)
        # status_text_in.send_keys(Keys.RETURN)

    def random_likes(self):
        while True:
            rand_num = randrange(0, 8)

            if rand_num % 4 == 0:
                pass
                

    def wait(self, delay=3):
        self.driver.implicitly_wait(delay)

    def close(self):
        self.driver.close()


