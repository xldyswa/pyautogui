import asyncio
import pyautogui
import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TARGET_IMAGE = "target1.png"
REFRESH_IMAGE = "target2.png"
SENT_IMAGE = "target4.png"
CLICK_IMAGE = "target5.png"


def find_target_on_screen(target_image_path):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    target = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.80
    if max_val >= threshold:
        return True, max_loc
    return False, None

async def check_for_new_message():

    while True:
        found, location = find_target_on_screen(TARGET_IMAGE)
        if found:
            print(f"检测到新信息,位置：{location}")
            found1, location = find_target_on_screen(CLICK_IMAGE)
            if found1:
                pyautogui.click(location[0], location[1])
            #pyautogui.press('1')
            pyautogui.write('Upwork has new messages!', interval=0.25)
            found2, location = find_target_on_screen(SENT_IMAGE)
            if found2:
                print("点击发送")
                pyautogui.click(location[0], location[1])

            await asyncio.sleep(600)  
        else:
            print("未检测到新信息...")
            await asyncio.sleep(5)

async def click_refresh_button():
    while True:
        found, location = find_target_on_screen(REFRESH_IMAGE)
        if found:
            pyautogui.click(location[0], location[1])
            print("点击刷新")
        else:
            print("未找到刷新按钮...")
        await asyncio.sleep(10)  

async def main():
    task1 = asyncio.create_task(check_for_new_message())
    task2 = asyncio.create_task(click_refresh_button())
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())
