import numpy as np
import cv2
import time

def create_border(frame, bordersize):
    row, col= frame.shape[:2]
    bottom= frame[row-2:row, 0:col]
    return cv2.copyMakeBorder(frame, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])

def grid_location(location, screen_center):
    x_pos, y_pos = location
    x_cen, y_cen = screen_center

    direction=""
   
    # Left or Right
    if (x_pos > screen_center[0]):
        direction+="RIGHT "
    else:
        direction+="LEFT "

    # Up or Down
    if (y_pos > screen_center[1]):
        direction+="DOWN"
    else:
        direction+="UP"

    return direction
    

def recticle(frame, x,y,w,h,color, thickness):

    center = (int(x+w/2), int(y+h/2))
   
    # X - Center
    cv2.line(frame, center, (x+w,y+h), color, thickness)
    cv2.line(frame, center, (x+w,y),   color, thickness)
    cv2.line(frame, center, (x,y+h),   color, thickness)
    cv2.line(frame, center, (x,y),     color, thickness)
    
    
    frame = cv2.rectangle(frame, (x,y), (x+w, y+h), font_color, 8)

    return frame


# Initializations
cap        = cv2.VideoCapture(0)
font_name  = cv2.FONT_HERSHEY_SIMPLEX
font_size  = .4        # Small 
font_color = (0,255,0) # Green
thickness  = 1
line_type  = cv2.LINE_AA

curr_time = 0.0

# --- --- Color Layers
LOWER_RED = np.array([70,140, 100])# R G B
UPPER_RED = np.array([140,255,255])# R G B

while True:

    font_color = (0,255,0)
    # Size Parameters
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    center = (int(width/2),int(height/2))

    
    _, frame = cap.read()

    # --- HSV Filtering
    
    # --- --- blur frame
    blurred = cv2.GaussianBlur(frame, (11,11), 0)

    # --- --- convert hsv
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # --- --- construct mask
    mask = cv2.inRange(hsv, LOWER_RED, UPPER_RED)

    # --- --- perform erosion
    mask = cv2.erode(mask, None, iterations=2)

    # --- --- perform dilation
    mask = cv2.dilate(mask, None, iterations=2) 

    # --- --- perform contour
    
    contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    status    = "NONE"
    Direction = 'NONE'

    if len(contours)>0:



        status = "DISCOVERED" 
        cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)

        x_center=x+w/2
        y_center=y+h/2
         
        Direction = grid_location(center, (int(x+w/2), int(y+h/2)))


        if abs(x_center - center[0]) <50 and abs(y_center - center[1]) <50:
            status     = "LOCK"
            font_color = (0, 0, 255)
            Direction  = "LOCKED"
        
        frame = recticle(frame, x, y, w, h, font_color, 2)

        
    # --- --- Return the Frame

    # FPS on Frame
    prev_time = curr_time
    curr_time = time.time()

    fps = 1/abs(prev_time - curr_time);
    
    

    # HUD

    # --- Text

    HEADER_TEXT    = '###########'
    formatted_text1='FPS:{0:18.2f}'
    target_status  ='TARGET:{:>13}'
    formatted_text3='ORIENTATION:{:>8}'


    # cv2.putText(frame, formatted_text1.format(fps),(25, 25), font_name, font_size, (0,255,0), thickness, line_type)
    cv2.putText(frame, target_status.format(status), (25, 50), font_name, font_size, font_color,thickness, line_type)
    cv2.putText(frame, formatted_text3.format(Direction),(25, 75), font_name, font_size, font_color, thickness, line_type)
     
    # --- Visualizations

    # --- --- Left side
    cv2.line(frame, (62, int((1/4)*height)-18), (25, int((1/4)*height)), font_color, 2)
    cv2.line(frame, (25, int((1/4)*height)), (25, int((3/4)*height)), font_color, 2)
    cv2.line(frame, (25, int((3/4)*height)),(62, int((3/4)*height)+18), font_color, 2)

    # --- --- Right Side
    cv2.line(frame, (int(width) - 62, int((1/4)*height)-18), (int(width) - 25, int((1/4)*height)),  font_color, 2)
    cv2.line(frame, (int(width) - 25, int((1/4)*height)),    (int(width) - 25, int((3/4)*height)), font_color, 2)
    cv2.line(frame, (int(width) - 25, int((3/4)*height)),    (int(width) - 62, int((3/4)*height)+18), font_color, 2)

    # --- --- Crosshair
    cv2.line(frame, center, (center[0], center[1]+10), font_color, 2)
    cv2.line(frame, center, (center[0], center[1]-10), font_color, 2)
    cv2.line(frame, center, (center[0]+10, center[1]), font_color, 2)
    cv2.line(frame, center, (center[0]-10, center[1]), font_color, 2)


    frame_w_border = create_border(frame, bordersize=10)
    # Show Frame
    cv2.imshow("Capture", frame_w_border)
    if cv2.waitKey(1) == ord('q'):
        cap.destroyAllWindows
        cap.release()
