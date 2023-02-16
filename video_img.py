from itertools import count
import pafy
import cv2
path = 'image/'
url = 
video = pafy.new(url)
print(video.videostreams)
# best = video.getbest()
best = video.videostreams[-1]
capture = cv2.VideoCapture(best.url)
fps = capture.get(cv2.CAP_PROP_FPS)
start = fps*(0 * 60 + 0)
print(start)
capture.set(1, start)
# total = ((fps*(20 * 60 + 0)) - start) / 4
# print(total)
ret, frame = capture.read()
count = 1
curr_count = 0
while ret:
    filename = "jpg_" + str(count) + ".jpg"
    cv2.imwrite(path + filename, frame)
    count += 1
    for i in range(int(fps * 5)):
        ret, frame = capture.read()
    curr_count += 1
print(count)
print("finish")
