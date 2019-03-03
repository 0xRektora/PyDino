import cv2
import PIL.ImageGrab
import PIL.ImageOps
import numpy as np
import time
import pyautogui
from matplotlib import pyplot as plt

size_game = (775, 536)
scan_area = [165, 40]
void_area = (40,40)
template = cv2.imread('data/dino2.png')
pyautogui.PAUSE = 0.1

# screen = PIL.ImageGrab.grab()
# screen = np.array(screen)

# screen = cv2.resize(screen, size_game)
# cv2.imwrite('data/result22.png', screen)

# w, h = template.shape[:-1]

# res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
# threshold = .7
# loc = np.where(res >= threshold)
# for pt in zip(*loc[::-1]):  # Switch collumns and rows
#     cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

# cv2.imwrite('data/result.png', screen)
import datetime
screen=0
w, h = 0, 0
res = 0
threshold = 0
loc = 0
scan_x = 0
scan_y = 0
scan = 0

def grayConversion(image):
    grayValue = 0.07 * image[:,:,2] + 0.72 * image[:,:,1] + 0.21 * image[:,:,0]
    gray_img = grayValue.astype(np.uint8)
    return gray_img


while True:
    
    start = time.time()
    print(datetime.datetime.now())
    screen = PIL.ImageGrab.grab()
    print(np.array(PIL.ImageOps.grayscale(screen).getcolors()).sum())
    screen = np.array(screen)

    screen = cv2.resize(screen, size_game)

    w, h = template.shape[:-1]

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = .7
    loc = np.where(res >= threshold)
    # for pt in zip(*loc[::-1]):  # Switch collumns and rows
    #     cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)


    if len(loc[0]):
        print("Player found")

        scan_x = loc[::-1][0][0] + w
        scan_y = (loc[::-1][1][0]) - 10
        print(scan_x, scan_y)

        scan = screen[scan_y: scan_y + scan_area[1], scan_x: scan_x + scan_area[0]]
        cv2.imwrite('data/scan.png', scan)
        print(scan)
        break

    else:
        print("Player not found")
    print("Process in,", time.time()-start)

startpoint = time.time()
while True:
    start = time.time()
    
    print( time.time() - startpoint  )

    if  time.time()- startpoint  >= 5. and scan_area[0] < 300:
        startpoint = time.time()
        scan_area[0] += 10
        print("ADDED")

    print(" SCAN ", scan_area[0])

    print(datetime.datetime.now())
    
    screen = PIL.ImageGrab.grab()

    screen = np.array(screen)

    screen = cv2.resize(screen, size_game)

    w, h = template.shape[:-1]

    print("found")

    scan_x = loc[::-1][0][0] + w
    scan_y = loc[::-1][1][0]
    # print(scan_x, scan_y)

    print(screen.shape)
    print(scan_y + scan_area[1]/2)
    scan = screen[scan_y + int(scan_area[1]/2): scan_y + scan_area[1], scan_x + int(scan_area[0]/2): scan_x + scan_area[0]]
    # void = screen[scan_y: scan_y + int(scan_area[1]/2), scan_x: scan_x + int(scan_area[0]/2)]
    
    edges = cv2.Canny(scan,100,200)

    # plt.subplot(121),plt.imshow(scan,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

    # plt.show()

    # gray = grayConversion(scan)
    # gray_void = grayConversion(void)
    
    # graySum = np.array(gray).sum()
    # grayVoidSum = np.array(gray_void).sum()

    # print("Gray:", graySum)

    # cv2.imwrite('data/scan.png', scan)
    # print(scan)
    
    #Gray white 1836000
    # [83, 83, 83] in scan.reshape(-1, 3)
    # if  graySum != grayVoidSum:
    #     pyautogui.press('space')
    #     print("object detected")

    if  np.any(edges > 0):
        pyautogui.press('space')
        print("object detected")

    # else:
        # print('no obstacle')
    
    # test detect
    # cv2.rectangle(screen, (scan_x, scan_y), (scan_x + scan_area[0], scan_y + scan_area[1]), (0, 0, 255), 2)
    # cv2.rectangle(screen, (scan_x, scan_y), (scan_x + void_area[0], scan_y + void_area[1]), (0, 0, 255), 2)
    # cv2.imwrite('data/result.png', screen)
    # break

    
    print("Process in,", time.time()-start)