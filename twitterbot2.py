from selenium import webdriver
from selenium import common
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time, os

class Twitterbot:

  def __init__(self):

    """Constructor
    """

    # initializing chrome options
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument("headless")

    # adding the path to the chrome driver and
    # integrating chrome_options with the bot
    # service = Service(os.path.join(os.getcwd(), 'chromedriver'))  
    self.bot = webdriver.Chrome(  options = chrome_options)
    self.bot.set_page_load_timeout(30)


  def open_a_twitter_link(self, link, scroll_to):
    bot = self.bot
    try:
      bot.get(link)
      time.sleep(8)
      for pix in range(500, scroll_to + 1, 500):
        script = "window.scroll(0,'{}');".format(pix)
        bot.execute_script(script)
        time.sleep(1)
      return bot.find_element(by=By.XPATH, value='//div[@data-testid="tweetText"]').text
    except TimeoutException as ex:
      print("Exception has been thrown. " + str(ex))
      print("continuing ...")


