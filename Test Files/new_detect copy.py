import torch
import numpy as np
import cv2
import ffmpeg
import pafy
from time import time
from selenium import webdriver
import subprocess as sp

class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using OpenCV.
    """
    
    def __init__(self, url, model_name):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param img: A valid output file name.
        """
        self.model = self.load_model(model_name)
        self.FFMPEG_BIN = "ffmpeg"
        self.classes = self.model.names
        self.URL = url
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

    
    def get_video_from_url(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        pipe = sp.Popen([ self.FFMPEG_BIN, "-i", self.URL,
            "-loglevel", "quiet", # no text output
            "-an",   # disable audio
            "-f", "image2pipe",
            "-pix_fmt", "bgr24",
            "-vcodec", "rawvideo", "-"],
            stdin = sp.PIPE, stdout = sp.PIPE)
        
        return pipe


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


    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.01:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
        
        return frame

    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        X,Y = 1920,1080
        player = self.get_video_from_url()

        while True:
            raw_image = player.stdout.read(X*Y*3)
            frame =  np.fromstring(raw_image, dtype='uint8').reshape((Y,X,3))
            cv2.imshow('Results',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()

# Create a new object and execute.
detection = ObjectDetection("https://ewcdnsite06.nowe.com/session/09-99d16f35a69a8933173b9b21d0ef4/Content/HLS/LIVE/Channel(HLS_CH332N)/Stream(02)/index.m3u8", "/Users/saharsh/Desktop/Ad_Detect/NowTV/nowtv_best.pt")
detection()