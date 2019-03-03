import cv2
import numpy as np
import PIL.ImageGrab
import pyautogui
import datetime
import time
from matplotlib import pyplot as plt

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

# GAME_SIZE = (775, 536) # The screen size to reshape 
AREA_SCAN = [0, 0] # The "FoV" of the player

DINO = cv2.imread('data/player.png')
GAME = cv2.imread('data/game.png')

AREA_SCAN[1], AREA_SCAN[0] = GAME.shape[:-1]
AREA_SCAN[0] =  int(AREA_SCAN[0] * 15 / 100)
AREA_SCAN[1] = int(DINO.shape[:-1][0] * (3/2))

AREA_SCAN_ADDER = int(AREA_SCAN[0] * 5 / 100)
AREA_SCAN_MAX = int(GAME.shape[:-1][1] * 30 / 100)

print("[+] Screen : ", GAME.shape[:-1])
print("[+] Max area scan : ", AREA_SCAN_MAX, "[+] Scan area :", AREA_SCAN,"[+] Area scan adder", AREA_SCAN_ADDER)

w, h = 0, 0

scan_x = 0
scan_y = 0

scan = 0

print("[+] Looking for player.")


while True:
    screen = PIL.ImageGrab.grab()
    screen = np.array(screen)

    res = cv2.matchTemplate(screen, DINO, cv2.TM_CCOEFF_NORMED)
    threshold = .8
    loc = np.where(res >= threshold)

    if len(loc[0]):
        print("[+] Player found")

        scan_x = loc[::-1][0][0] + w
        scan_y = loc[::-1][1][0]
        
        scan = screen[scan_y: scan_y + AREA_SCAN[1], scan_x: scan_x + AREA_SCAN[0]]
        break


startpoint = time.time()
while True:
    start = time.time()

    if  time.time()- startpoint  >= 10. and AREA_SCAN[0] < AREA_SCAN_MAX:
        startpoint = time.time()
        AREA_SCAN[0] += AREA_SCAN_ADDER
        
    
    screen = PIL.ImageGrab.grab()

    screen = np.array(screen)

    h, w = DINO.shape[:-1]

    scan_x = loc[::-1][0][0] + (w*2)
    scan_y = loc[::-1][1][0]

    scan = screen[scan_y : scan_y + AREA_SCAN[1], scan_x: scan_x + AREA_SCAN[0]]
    
    # cv2.rectangle(screen, (scan_x, scan_y), (scan_x + AREA_SCAN[0], scan_y + AREA_SCAN[1]), (0, 0, 255), 2)
    # cv2.imwrite('data/result.png', screen)
    # break

    edges = auto_canny(scan)

    if  np.any(edges[int(edges.shape[0]/4):int(edges.shape[0]/(3/2)) , int(edges.shape[1]/4):int(edges.shape[1]/(3/2)) ] > 0):
        pyautogui.press('space')
        print("[+] Object detected")

    print("[+] Process in,", time.time() - start)

