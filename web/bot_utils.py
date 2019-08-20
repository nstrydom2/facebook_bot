from config import acct_conf

from random import randrange
from logging import getLogger


class BotUtils():
    def __init__(self):
        self.utils_logger = getLogger(__name__)

        self.fb_url = None
        self.driver = None

    def login_required(self, func):
        def wrapper():
            menu_button_xpath = '/html/body/div/div/div[1]/div/div/a[8]'

            menu_button = self.driver.find_element_by_xpath(menu_button_xpath)

            if menu_button is None:
                self.login()

        return wrapper

    def friends_page_required(self, func):
        def wrapper():
            if not self.driver.current_url.index('friends') >= 0:
                self.load_friends_requests()

        return wrapper

    @login_required
    def load_fb(self):
        self.driver.get(self.fb_url)
        self.wait()

    @login_required
    def load_wall(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[1]/div[1]/h1/a/span').click()
        self.wait()

    @login_required
    def load_profile(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/a'
        ).click()
        self.wait()

    # Login to facebook
    def login(self, usr=acct_conf.USER, passwd=acct_conf.PASS):
        email_element = self.driver.find_element_by_name('email')
        pass_element = self.driver.find_element_by_name('pass')

        email_element.send_keys(usr)
        pass_element.send_keys(passwd)

        self.driver.find_element_by_name('login').click()
        self.wait(5)

        self.driver.find_element_by_xpath('/html/body/div/div/div/div/table/tbody/tr/td/div/div[3]/a').click()
        self.wait(5)

    @login_required
    def load_friends_requests(self):
        friends_button_xpath = '/html/body/div/div/div[1]/div/div/a[6]'
        friend_requests_xpath = '/html/body/div/div/div[2]/div/div[1]/div[1]/a'

        # Click friend requests button
        self.driver.find_element_by_xpath(friends_button_xpath).click()
        self.wait()

        # Click 'See All' in friend requests drop down
        self.driver.find_element_by_xpath(friend_requests_xpath).click()
        self.wait()

    @login_required
    def like_post(self, num_post=0):
        post_xpath = '/html/body/div/div/div[2]/div/div[4]/div[3]/div[{0}]/div[2]/div[2]/span[1]/a[1]'.format(num_post)

        try:
            self.driver.find_element_by_xpath(post_xpath).click()
            self.wait()

        except:
            pass

    @login_required
    def random_like(self, max=50):
        rand_num = randrange(0, max)

        self.like_post(rand_num)

    @friends_page_required
    def accept_friend_request(self, request_xpath, index=0):
        if request_xpath is None:
            request_xpath = ''.format(index)

        self.driver.find_element_by_xpath(request_xpath).click()
        self.wait()

    @friends_page_required
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
            self.utils_logger.error('Error --> ' + ex)

    def wait(self, delay=3):
        self.driver.implicitly_wait(delay)

    def close(self):
        self.driver.close()

