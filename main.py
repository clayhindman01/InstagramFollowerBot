from selenium import webdriver;
from time import sleep;

# Will need to create a secrets.py file and save your instagram username and password in variables.
from secrets import username, password;

class FollowerBot:
    def __init__(self, username, password):

        # Set username so it can be used in other methods
        self.username = username
        self.driver = webdriver.Chrome("C:\\Users\clayh\chromedriver_win32\chromedriver.exe");

        # Open instagram and log in
        self.driver.set_window_size(1920,1080);
        self.driver.get("https://instagram.com");
        sleep(1);
        self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[1]/div/label/input").send_keys(username);
        self.driver.find_element_by_xpath("//*[@id=\"loginForm\"]/div/div[2]/div/label/input").send_keys(password);
        self.driver.find_element_by_xpath('//button[@type="submit"]').click();
        sleep(4)
        self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click();

    # Check who is following you.
    def check_unfollows(self): 
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        sleep(2)

        #Get users that you are following
        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        following = self._get_names_following()
        
        # Get the users that are following you
        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        followers = self._get_names_followers()

        # Compare the users that are following you and the users that you are following
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    # Get the names of users you are following.
    def _get_names_following(self):
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[3]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0,arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name("a")
        following = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()
        return following

    # Get names of users following you.
    # Getting names of followers and following had to be split into 2 functions becuase the scrollbar had a different xpath so it wouldn't work for both.
    def _get_names_followers(self):
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0,arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name("a")
        followers = [name.text for name in links if name.text != '']
        self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()
        return followers

instagram_bot = FollowerBot(username, password);
instagram_bot.check_unfollows()
