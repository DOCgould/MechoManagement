import cv2
import numpy as np

BORDER_SIZE        = 10
AREA_THRESHOLD     = 1000
DISTANCE_THRESHOLD = 100
FONT               = cv2.FONT_HERSHEY_SIMPLEX
FONT_SIZE          = 1

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    # HSV Filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # This should detect a red object (Or turquoise)
    # The values for HSV were taken from online as I wanted to spend time on
    # the rest of the process
    lower_hsv = np.array([30,150,50])
    upper_hsv = np.array([255,255,180])
    mask      = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Finding the contours from the hsv mask
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # Taking the largest of the contours
    # In the future it would be nice to just work with all objects above the threshold
    largest_area  = 0
    largest_index = -1
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])
        if area > largest_area:
            largest_area  = area
            largest_index = i

    # This determines if an object was detected
    if largest_index > -1 and largest_area > AREA_THRESHOLD:
        # Creating the bounding box around the contour
        x,y,w,h = cv2.boundingRect(contours[largest_index])
        # I drew this for debugging and decided to keep it active as it is
        # useful to visualize
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 3)

        # Computing the images center coordinates
        im_cx = frame.shape[1]/2
        im_cy = frame.shape[0]/2
        # Computing the objects center coordintes
        cx = x + w/2
        cy = y + h/2

        # Draw Target
        cv2.circle(frame, (int(cx), int(cy)), 20, (0,0,255),-1)
        cv2.circle(frame, (int(cx), int(cy)), 10, (255,255,255),-1)
        cv2.circle(frame, (int(cx), int(cy)), 5, (0,0,255),-1)

        # Gathering locational information and creating text describing the
        # location of the object.
        horizontal_text = ""
        vertical_text   = ""
        display_text = "Turn Camera "
        if cx - im_cx > DISTANCE_THRESHOLD:
            horizontal_text = "left"
        elif im_cx - cx > DISTANCE_THRESHOLD:
            horizontal_text = "right"
        if cy - im_cy > DISTANCE_THRESHOLD:
            vertical_text = "down"
        elif im_cy - cy > DISTANCE_THRESHOLD:
            vertical_text = "up"

        if horizontal_text == "" or vertical_text == "":
            if horizontal_text == "" and vertical_text == "":
                display_text = "Alligned"
            else:
                display_text += "{}{}".format(horizontal_text, vertical_text)
        else:
            display_text += "{} and {}".format(horizontal_text, vertical_text)
             
        cv2.putText(frame, display_text, (0,50), FONT, FONT_SIZE, (255,255,255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Object Not Found", (0,50), FONT, FONT_SIZE, (255,255,255), 2, cv2.LINE_AA)
        

    # Puts the border around the image
    border_img = cv2.copyMakeBorder(frame, top=BORDER_SIZE, bottom=BORDER_SIZE, left=BORDER_SIZE,
            right=BORDER_SIZE, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])

    cv2.imshow("frame", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cv2.destroyAllWindows()
cap.release() 
