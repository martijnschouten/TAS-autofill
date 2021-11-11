from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import yaml
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    with open('settings.yaml', 'r') as stream:
            settings_dict = yaml.safe_load(stream)
except:
    raise ValueError("Could not find a settings.yaml file. Make sure there is a settings.yaml file with your settings")

if 'email' in settings_dict:
    email = settings_dict['email']
else:
    raise ValueError("Could not find an email.")

if 'password' in settings_dict:
    password = settings_dict['password']
else:
    raise ValueError("Could not find an password.")

if 'project_number' in settings_dict:
    project_number = settings_dict['project_number']
else:
    raise ValueError("Could not find an project_number.")

if 'work_hours' in settings_dict:
    work_hours = float(settings_dict['work_hours'])
else:
    raise ValueError("Could not find  work_hours.")

options = webdriver.ChromeOptions()
if len(sys.argv) > 1: 
    if sys.argv[1] == '--headless':
        options.add_argument('--headless')

driver = webdriver.Chrome('./chromedriver',options=options)
driver.get("https://webapps.utwente.nl/tas/en/tasservlet")

delay = 5 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
time.sleep(1)
login = driver.find_element(By.NAME,"loginfmt")
login.clear()
login.send_keys(email)
login.send_keys(Keys.RETURN)

try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'passwd')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
time.sleep(2)
login = driver.find_element(By.NAME,"passwd")
login.clear()
login.send_keys(password)
login.send_keys(Keys.RETURN)

delay = 10 # seconds
try:
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'urenDag1Totaal')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")
time.sleep(1)    

rows = driver.find_elements(By.NAME, "codeActiviteit")
leave_row = -1
project_row = -1
for i1 in range(len(rows)):
    if rows[i1].get_attribute("value") == '000-Leave':
        leave_row = i1
    if rows[i1].get_attribute("value") == project_number:
        project_row = i1

if project_row == -1:
    raise RuntimeError("Could not find a row related to your project number. Please add your project manually")

while True:
    empty = False
    for i1 in range(5):
        if leave_row == -1:
            project_cell = driver.find_element(By.ID, "urenDag"+str(i1+1)+'_'+str(project_row))
            if project_cell.get_attribute('value')=='':
                project_cell.send_keys(str(work_hours))
                empty = True
        else:
            leave_cell = driver.find_element(By.ID,"urenDag"+str(i1+1)+'_'+str(leave_row))
            leave_string = leave_cell.get_attribute("value")
            if leave_string == '' :
                leave = 0
            else:
                leave = float(leave_string)

            project_cell = driver.find_element(By.ID,"urenDag"+str(i1+1)+'_'+str(project_row))
            if project_cell.get_attribute('value')=='':
                project_cell.send_keys(str(work_hours-leave))
                empty = True
    if empty:
        driver.find_element(By.ID,"btnSave_0").click()
        time.sleep(0.1)
        driver.find_element(By.XPATH,"/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/form/fieldset/table/tbody/tr/td[1]/button").click()
        time.sleep(0.1)
        driver.find_element(By.XPATH,"/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/form/table[1]/tbody/tr/td[3]/table/tbody/tr/td[1]/button").click()
        time.sleep(1)
    else:
        break