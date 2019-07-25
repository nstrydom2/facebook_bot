from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Bot():
    def __init__(self):
        # Prob create selenium instance here
        self.driver = webdriver.Firefox(executable_path=r'/home/ghost/Drivers/geckodriver')

    def load_fb(self):
        self.driver.get('https://facebook.com/')
        self.wait()

    # Login to facebook
    def login(self, usr, passwd):
        email_element = self.driver.find_element_by_name('email')
        pass_element = self.driver.find_element_by_name('pass')

        email_element.send_keys(usr)
        pass_element.send_keys(passwd)

        self.driver.find_element_by_xpath('//*[@id="u_0_2"]').click()
        self.wait()

    def load_friends_requests(self):
        # Click friend requests button
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]'
        ).click()
        self.wait()

        # Click 'See All' in friend requests drop down
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div/ul/li/div/div/div[2]/a'
        ).click()
        self.wait()

    def add_recommended(self, limit=150):
        self.load_friends_requests()

        try:
            for friend in range(1, limit):
                # Click on 'Add Friend' button of recommended friend
                self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div[3]/div[1]/div/div[1]/div[2]/div[2]/div/form/div/div/div[1]/ul[1]/li[' /
                    + str(friend) + ']/div/div/div/div[2]/div[2]/div/div/div/div/div/button[1]'
                ).click()
                self.wait()
        except:
            pass


    def accept_all_friend_requests(self):
        self.load_friends_requests()
        pass

    def wait(self, delay=3):
        self.driver.implicitly_wait(delay)

    def close(self):
        self.driver.close()


