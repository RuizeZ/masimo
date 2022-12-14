from itertools import count
import pafy
import cv2
path = 'C:/Users/ruize.zhang/Desktop/youtubeImg/video_hand_sanitizing_images/'
url = "https://www.youtube.com/watch?v=m4z9w6nOBV0"
video = pafy.new(url)
best = video.getbest()
capture = cv2.VideoCapture(best.url)
fps = capture.get(cv2.CAP_PROP_FPS)
start = fps*(0 * 60 + 40)
print(start)
capture.set(1, start)
total = ((fps*(20 * 60 + 0)) - start) / 4
print(total)
ret, frame = capture.read()
count = 9725 + 1
curr_count = 0
while ret and curr_count <= total:
    filename = "jpg_" + str(count) + ".jpg"
    cv2.imwrite(path + filename, frame)
    count += 1
    for i in range(int(fps / 3)):
        ret, frame = capture.read()
    curr_count += 1
print(count)
print("finish")
