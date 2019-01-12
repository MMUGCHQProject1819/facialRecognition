import numpy as np
import cv2

template = cv2.imread('eye.jpg', 0) #turns image into gray scale
frame = cv2.imread("face.jpg", 0)

cv2.imshow("Frame", frame)
cv2.imshow("Template", template)

result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED) #compares and stores the asnwer on result

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result) #calculate brightest spot in the grayscale (brightest means highest match)
print(max_val, max_loc)
cv2.circle(result, max_loc, 15, 255, 2) #circles brightest spot in result picture
cv2.imshow("Matching", result)

cv2.waitKey(0)
cv2.destroyAllWindows()