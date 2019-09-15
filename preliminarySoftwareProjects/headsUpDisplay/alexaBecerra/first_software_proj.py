import cv2
import numpy as np
import imutils
from PIL import Image

def print(text, frame):
    cv2.putText(frame, text, (50, 75), cv2.FONT_HERSHEY_PLAIN, 2, (25, 150, 0), 2)

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    #Converting HUD from RGB to BGR
    hud = Image.open('Halo3Hud.png').convert('RGBA')
    R,G,B,A = hud.split()
    hud = Image.merge('RGBA', (B,G,R,A))

    #Color Red Values
    low_red1= np.array([0, 180, 180])
    high_red1 = np.array([10, 255, 255])
    low_red2 = np.array([170, 180, 180])
    high_red2 = np.array([180, 255, 255])

    while True:
        _,frame = cam.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        red_mask1 = cv2.inRange(hsv_frame, low_red1, high_red1)
        red_mask2 = cv2.inRange(hsv_frame, low_red2, high_red2)
        final_mask = red_mask1 + red_mask2
        red = cv2.bitwise_and(frame, frame, mask=final_mask)

        _,thresh = cv2.threshold(final_mask, 40, 255, 0)
        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        #Get 10 largest contours
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

        #Attaching HUD to frame
        pil_img = Image.fromarray(frame)
        pil_img.paste(hud, mask=hud)

        if len(contours) != 0:
            #find biggest area
            c = max(contours, key=cv2.contourArea)

            #Only detect areas above certain size, to filter undesirable detections
            if cv2.contourArea(c) > 100:
                x,y,w,h, = cv2.boundingRect(c)
                #Draw box in blue
                cv2.rectangle(frame, (x,y), (x+w,y+h), (200, 15, 0), 5)
                cv2.line(frame, (x,y+h), (x+w, y), (200, 100, 0), 3)
                cv2.line(frame, (x,y), (x+w, y+h), (200, 100, 0), 3)

                #Change x & y for center of detection
                x = x + (w/2)
                y = y + (h/2)

                if x > 561 and x < 743:
                    if y > 466:
                        print("MOVE DOWN", frame)

                    if y < 284:
                        print('MOVE UP', frame)

                elif y > 284 and y < 466:
                    if x > 743:
                        print('MOVE RIGHT', frame)

                    if x < 561:
                        print('MOVE LEFT', frame)

                elif x > 743 and y > 466:
                    print('MOVE DOWN-RIGHT', frame)

                elif x > 743 and y < 284:
                    print('MOVE UP-RIGHT', frame)

                elif x < 561 and y > 466:
                    print("MOVE DOWN-LEFT", frame)

                elif x < 561 and y < 466:
                    print('MOVE UP-LEFT', frame)


        #Attaching HUD to frame
        pil_img = Image.fromarray(frame)
        pil_img.paste(hud, mask=hud)
        frame = np.array(pil_img)

        #Center reticle
        cv2.line(frame, (645, 375), (659, 375), (250, 40, 0), 2)
        cv2.line(frame, (652, 382), (652, 368), (250, 40, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
