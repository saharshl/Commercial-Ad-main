from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

yoururl = "https://news.now.com/home/live"

options = webdriver.ChromeOptions()
options.add_argument("headless")
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(ChromeDriverManager().install(),desired_capabilities=caps, chrome_options=options)

driver.get(yoururl)
time.sleep(10) # wait for all the data to arrive. 
perf = driver.get_log('performance')

def get_all_keys(d):
    for key, value in d.items():
        if "url" in key:
            if "Stream(02)" in value:
                yield value
      
        try:
            evald = json.loads(str(value))
            if isinstance(evald, dict):
                # f2.write(str(evald)+'\n')
                d[key] = evald
                yield from get_all_keys(evald)
          
        except (SyntaxError, ValueError, AssertionError):
            pass
        
        if isinstance(value, dict):
            yield from get_all_keys(value)  
          
        if isinstance(value,list):
            for i in value:
                if isinstance(i,dict):
                    yield from get_all_keys(i)

for d in perf: 
    for x in get_all_keys(d):
        print(x)

driver.quit()