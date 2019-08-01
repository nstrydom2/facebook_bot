from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType

from config import proxy as proxy_conf

class Bot():
    def __init__(self, proxy=False):
        browser_profile = webdriver.FirefoxProfile()
        browser_profile.set_preference('dom.webnotifications.enabled', False)

        # Prob create selenium instance here
        if proxy is False:
            self.driver = webdriver.Firefox(executable_path=r'/home/ghost/Drivers/geckodriver',
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

            self.driver = webdriver.Firefox(executable_path=r'/home/ghost/Drivers/geckodriver',
                                            firefox_profile=browser_profile,
                                            desired_capabilities=capabilities)

    def load_fb(self):
        self.driver.get('https://mbasic.facebook.com/')
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

    def wait(self, delay=3):
        self.driver.implicitly_wait(delay)

    def close(self):
        self.driver.close()


