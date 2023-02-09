import PyChromeDevTools
import time

chrome = PyChromeDevTools.ChromeInterface(host="1.1.1.1",port=8000)
chrome.Network.enable()
chrome.Page.enable()

start_time=time.time()
chrome.Page.navigate(url="http://www.google.com/")
chrome.wait_event("Page.loadEventFired", timeout=60)
end_time=time.time()

print ("Page Loading Time:", end_time-start_time)