import logging

from config import acct_conf

from random import randrange
from logging import getLogger


utils_logger = getLogger('facebook_bot.web.bot_utils')

class BotUtils():
    def __init__(self, driver, fb_url):
        self.fb_url = fb_url
        self.driver = driver

    def setup_module_log(self):
        stream_handler = logging.StreamHandler()

        if self.logger is not None or len(self.logger) != 0:
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
        utils_logger.addHandler()

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
        utils_logger.addHandler(stream_handler)

    def check_login(self):
        try:
            menu_button_xpath = '/html/body/div/div/div[1]/div/div/a[8]'
            menu_button = self.driver.find_element_by_xpath(menu_button_xpath)

        except:
            self.load_fb()
            self.login()

    def load_fb(self):
        try:
            self.driver.get(self.fb_url)
            self.wait()

        except Exception as ex:
            utils_logger.error(str(ex))

    def load_wall(self):
        self.check_login()

        try:
            self.driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/h1/a/span').click()
            self.wait()

        except Exception as ex:
            utils_logger.error(str(ex))

    def load_profile(self):
        self.check_login()
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a'
        ).click()
        self.wait()

    # Login to facebook
    def login(self, usr=acct_conf.USER, passwd=acct_conf.PASS):
        try:
            email_element = self.driver.find_element_by_name('email')
            pass_element = self.driver.find_element_by_name('pass')

            email_element.send_keys(usr)
            pass_element.send_keys(passwd)

            self.driver.find_element_by_name('login').click()
            self.wait(5)

            self.driver.find_element_by_xpath('/html/body/div/div/div/div/table/tbody/tr/td/div/div[3]/a').click()
            self.wait(5)

        except Exception as ex:
            utils_logger.error(str(ex))

    def load_friends_requests(self):
        self.check_login()

        try:
            friends_button_xpath = '/html/body/div/div/div[1]/div/div/a[6]'
            friend_requests_xpath = '/html/body/div/div/div[2]/div/div[1]/div[1]/a'

            # Click friend requests button
            self.driver.find_element_by_xpath(friends_button_xpath).click()
            self.wait()

            # Click 'See All' in friend requests drop down
            self.driver.find_element_by_xpath(friend_requests_xpath).click()
            self.wait()

        except Exception as ex:
            utils_logger.error(str(ex))

    def like_post(self, num_post=0):
        self.check_login()

        post_xpath = '/html/body/div/div/div[2]/div/div[4]/div[3]/div[{0}]/div[2]/div[2]/span[1]/a[1]'.format(num_post)

        try:
            self.driver.find_element_by_xpath(post_xpath).click()
            self.wait()

        except Exception as ex:
            utils_logger.error(str(ex))

    def random_like(self, max=50):
        self.check_login()

        rand_num = randrange(0, max)
        self.like_post(rand_num)

    def accept_friend_request(self, request_xpath, index=0):
        self.check_login()

        try:
            if request_xpath is None:
                request_xpath = ''.format(index)

            self.driver.find_element_by_xpath(request_xpath).click()
            self.wait()

        except Exception as ex:
            utils_logger.error(str(ex))

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

        except Exception as ex:
            utils_logger.error(str(ex))

    def upload_picture(self, caption='', img_path=''):
        upload_button_xpath = '//*[@id="js_1"]'
        upload_button_id = 'js_1il'
        upload_button_xpath = '/html/body/div/div/div[2]/div/div[2]/div/form/div[2]/span/div[1]/table/tbody/tr/td[2]/input'
        file_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/form/div[1]/div/input[1]'
        preview_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/form/div[3]/input[1]'
        post_button_xpath = '/html/body/div/div/div[2]/div/table/tbody/tr/td/div/form/input[19]'

        # self.driver.find_element_by_xpath(
        #     '/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div/div' +
        #     '/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/ul/li[1]/div/div/span/a'
        # ).click()

        self.driver.find_elements_by_id(upload_button_id).click()
        # Click Upload Photo link/button
        self.driver.find_elements_by_xpath(upload_button_xpath)[0].click()
        self.wait()
        #

        # Select Pic to upload
        self.driver.find_element_by_xpath(file_button_xpath)[0].click()
        self.wait()

        # Click Preview button
        self.driver.find_element_by_xpath(preview_button_xpath)[0].click()
        self.wait()

        # Click Post button
        self.driver.find_element_by_xpath(post_button_xpath)[0].click()

    def wait(self, delay=3):
        try:
            self.driver.implicitly_wait(delay)

        except Exception as ex:
            utils_logger.error(str(ex))

    def close(self):
        utils_logger.info('closing browser...')
        self.driver.close()

