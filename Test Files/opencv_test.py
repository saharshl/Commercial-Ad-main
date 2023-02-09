import cv2
import sys

url = 'https://ewcdnsite08.nowe.com/session/09-d70cda8c07f81d44149aaf58e73d1/Content/HLS/LIVE/Channel(HLS_CH332N)/Stream(02)/index.m3u8'

play = cv2.VideoCapture(url)
if (play.isOpened() == False):
    print('!!! Unable to open URL')
    sys.exit(-1)

fps = play.get(cv2.CAP_PROP_FPS)
wait_ms = int(1000/fps)
print('FPS:', fps)

while True:
    
    ret, frame = play.read()
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(wait_ms) & 0xFF==ord('q'):
        break

play.release()
cv2.destroyAllWindows()

wfc = 'https://spbtv.online/channels/world_fashion_channel.html'