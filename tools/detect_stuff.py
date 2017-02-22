# Ported From: http://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html
import os
import cv2

cascade = cv2.CascadeClassifier('/home/matt/Projects/opencv-junk/classifier/run_two/cascade_xmls/cascade.xml')
img_dir = '/mnt/jam-gui/smb-share:server=jamstation,share=gopro/2017-02-17/HERO4 Session 1/testing_frames'
img_files = [i for i in os.listdir(img_dir) if os.path.splitext(i)[1] == '.jpg']

## Single Detection
# img_file = 'GOPR0195_64000.jpg'
## Double Detection
# img_file = 'GP010195_200.jpg'

## Test that the rec will detect a large positive image used in training the cascade.
# img_dir = '/home/matt/Projects/opencv-sharrow-images/positives'
## LARGE TRAINING POSITIVE, WILL DETECT IN CURRENT CASCADE
# img_file = '10.jpg'
## SMALL TRAINING POSITIVE, WON'T DETECT IN CURRENT CASCADE
# img_file = 'GP010194_71100.jpg'

for img_file in img_files:
    img = cv2.imread(os.path.join(img_dir, img_file))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
