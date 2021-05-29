import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start","End"])

# 0 mean built in camera of laptop,if other camera installed, it will be 1,2 or 3
# you can place video file here: video=cv2.VideoCapture("movie.mp4") 
video=cv2.VideoCapture(0) 

number_frame = 0
while True:
    number_frame += 1
    
    check, frame = video.read()

    #time.sleep(3)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #blur image, (21,21) is width and height of a Gaussian kernel
    gray = cv2.GaussianBlur(gray,(21,21),0)

    # camera on mac: 10 first frame is black frame so we ignore it
    if number_frame < 10 :
        continue
    
    if first_frame is None :
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame,gray)
    
    # any pixel >35 will be white(255), other is black
    # return tuple with 2 values
    # thresh_binary use [1] for frame
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (image, contours, hierarchy) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    status = 0
    for contour in contours :
        if cv2.contourArea(contour) >= 10000 :
            status = 1
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    status_list.append(status)

    if (status_list[-1]==0) and (status_list[-2]==1) :
        times.append(datetime.now())
    if (status_list[-1]==1) and (status_list[-2]==0) :
        times.append(datetime.now())

    cv2.imshow("Gray",gray)
    cv2.imshow("Delta",delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame",frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1 :
            times.append(datetime.now())
        break;

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]},ignore_index=True)

df.to_csv("times.csv")

video.release()
cv2.destroyAllWindows()
