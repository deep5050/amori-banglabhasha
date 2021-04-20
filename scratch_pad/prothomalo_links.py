import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import shutil
from random import randint
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options




url = "https://www.prothomalo.com/onnoalo/stories"
base_url = "https://www.prothomalo.com"


# if chromedriver is not added to the PATH, uncomment the below line
# webdriver.Chrome(executable_path="./driver/")
options = webdriver.ChromeOptions()

options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f"user-agent={userAgent}")
options.add_argument("headless")  # headless mode, suitable for CI/CD

browser = webdriver.Chrome(chrome_options=options)
browser.get(url)

# scrolling to get the lazy-loading image src
lastHeight = browser.execute_script("return document.body.scrollHeight")
html = browser.page_source
browser.quit()

soup = BeautifulSoup(html,'lxml')


featured_story = soup.find_all('div',class_="six-stories-1widget-poll sixStories1WidgetWithPoll-m__base__2wht9")[0]
stories = featured_story.find_all('div',class_="story-data customStoryCard2-m__story-data__1s2ST")

f = open('urls','w')
for story in stories:
    link = story.find('a')['href']
    f.write(f"{link}\n")
f.close()

print("DONE :)")
