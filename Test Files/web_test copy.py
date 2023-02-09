import os
import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/Users/saharsh/Desktop/Ad_Detect/chromedriver')
driver.maximize_window()

driver.get('https://www.youtube.com/watch?v=t_jkcK5-2jQ')

driver.execute_script('window.open()')
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.youtube.com/watch?v=wmw6YyMie30')

count = 0
switch = 0

while True:
     if count == 0:
         driver.switch_to.window(driver.window_handles[0])
         count = 1
         time.sleep(3)
    
     else:
         driver.switch_to.window(driver.window_handles[1])
         count = 0
         time.sleep(3)
    
     print("executing")