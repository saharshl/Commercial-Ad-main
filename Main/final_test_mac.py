import cv2
import sys
from matplotlib.pyplot import flag
from webdriver_manager.chrome import ChromeDriverManager
import torch
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from timeit import default_timer as timer
import json

flagPointer = True

class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using OpenCV.
    """
    def __init__(self, model_name,tv_link):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param img: A valid output file name.
        """
        self.model = self.load_model(model_name)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(tv_link)
        self.driver.execute_script('window.open()')
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get('https://www.youtube.com/watch?v=wmw6YyMie30')
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.classes = self.model.names
        self.URL = tv_link
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nDevice Used:",self.device)


    def load_model(self, model_name):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    
    def get_video_from_url(self, url):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        cap = cv2.VideoCapture(url)
        if (cap.isOpened() == False):
            print('!!! Unable to open URL')
            sys.exit(-1)
        
        return cap


    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
     
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord


    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]


    def detect_ads(self, results):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        global flagPointer
        labels, cord = results
        n = len(labels)
        if n == 0:
            if flagPointer == True:
                self.driver.switch_to.window(self.driver.window_handles[1])
                self.driver.refresh()
                flagPointer = False
            return

        for i in range(n):
            row = cord[i]
            if row[4] >= 0.3:
                if flagPointer == False:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    flagPointer = True
    
    
    def new_url(self):

        yoururl = self.URL

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        browser = webdriver.Chrome(ChromeDriverManager().install(),desired_capabilities=caps, chrome_options=options)

        browser.get(yoururl)
        time.sleep(10) # wait for all the data to arrive. 
        perf = browser.get_log('performance')
        stream_list = list()

        def get_all_keys(d):

            for key, value in d.items():
                if "url" in key:
                    if "Stream(02)" in value: # this is only true for NowTV. TV channels have their own specific links. Need to manually understand what link to extract, and edit this line accordingly. 
                        if "m3u8" in value:
                            yield value
      
                try:
                    evald = json.loads(str(value))
                    if isinstance(evald, dict):
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
                stream_list.append(x)

        browser.quit()
        print("It worked!!")

        for a in stream_list:
            if a[-4:] == "m3u8": # Need to edit this line according to what specific link you want to extract (m3u8 or mpd) 
                return a

    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        start = timer()

        while True:
            # read one frame
            end = timer()
            if(int(end - start) > 1200 or int(end - start < 5)):
                readable_url = self.new_url()
                start = timer()

            player = self.get_video_from_url(readable_url)
            fps = player.get(cv2.CAP_PROP_FPS)
            wait_ms = int(1000/fps)
            fps_count = 0
            stream_count = 0
            
            while True:
            
                ret, frame = player.read()

                if not ret:
                    break

                if fps_count == (int(fps*2)):
                    results = self.score_frame(frame)
                    self.detect_ads(results)
                    fps_count = 0
            
                cv2.waitKey(wait_ms)
                
                if stream_count == (int(fps*20)):
                    break
                
                fps_count += 1
                stream_count +=1
            
            player.release()
            cv2.destroyAllWindows()

# Create a new object and execute.
tv_link = 'https://news.now.com/home/live'
detection = ObjectDetection('/Users/saharsh/Desktop/Ad_Detect/Commercial-Ad/Main/nowtv_best.pt',tv_link)
detection()