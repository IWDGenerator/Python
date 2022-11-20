from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys


pipes = json.load(open(sys.argv[1], 'r'))
for a in pipes:
    sluser = a['SLUsername']
    slpass = a['SLPass']
    pipelines = a['Pipelines']

options = Options()
options.add_argument('--no-sandbox') 
options.add_argument('--headless') 
options.add_argument("--window-size=1600x900")
#options.add_argument("--start-maximized")
print('options set')
driver = webdriver.Chrome(options=options)
print('driver set')

driver.get("https://elastic.snaplogic.com/sl/login.html")
time.sleep(3)
print("opening page completed")
user_field = driver.find_element(By.XPATH,'//*[@id="login-content"]/div/div[2]/div[2]/form/div[1]/input')
user_field.send_keys(sluser)
time.sleep(1)
print("user is entered")
pass_field = driver.find_element(By.XPATH,'//*[@id="login-content"]/div/div[2]/div[2]/form/div[2]/input')
pass_field.send_keys(slpass)
time.sleep(1)
print("pass is entered")
login_button = driver.find_element(By.XPATH,'//*[@id="login-content"]/div/div[2]/div[2]/form/div[3]/button')
login_button.click()
print("clicked login")


def assertpage():
    try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sl-wb-main"]')))
        print("Page is ready!")
    except TimeoutException:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        #mainpage = driver.find_element(By.XPATH,'//html')
        #mainpage.screenshot('/home/opt/snaplogic/screenshots/mainPage.png')
        print("Loading took too much time!")
        time.sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


assertpage()
print("successfully logged in")
time.sleep(1)



def open_pipe(pipename, pipeid):
    driver.get(f"https://elastic.snaplogic.com/sl/designer.html?v=d32de3#pipe_snode={pipeid}")
    assertpage()

    try:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
    except:
        print('no additional windows')

    try:
        driver.find_element(By.XPATH,'//*[@id="sl-menu-ctrl-vfit"]').click()
        time.sleep(4)
    except:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sl-menu-ctrl-vfit"]').click()
        time.sleep(4)

    def screenshot(pipelinename):
        pipe = driver.find_element(By.XPATH,'//*[@id="sl-wb-main"]')
        try:
            pipe.screenshot(f'/opt/snaplogic/screenshots/{pipelinename}.png')
            print('SC Taken')
        except:
            print('This pipeline has no snaps')

        close_pipe = driver.find_element(By.XPATH,'//*[@class="sl-tab-body sl-tab-draggable sl-x-select"]/div')
        close_pipe.click()

    screenshot(pipename)



for i in pipelines:
    try:
        open_pipe(i['name'], i['snode_id'])
    except AssertionError as error:
        exec_log.write(error)
        open_pipe(i['name'], i['snode_id'])
        time.sleep(1)


driver.close()
sys.exit()
