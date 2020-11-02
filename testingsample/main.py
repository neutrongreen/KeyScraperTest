import image_proccesing as ip
import os
import cv2
from datetime import datetime
import numpy as np
import time
import asyncio
import subprocess as sp
import pandas as pd
import pyautogui
from realtime_VideoStreamer import *

detected_keys = []
loop = asyncio.get_event_loop()
triggered = False
def log(string):
    now = datetime.now()
    print("[{a}] {b}".format(a = now.strftime("%d/%m/%Y %H:%M:%S"), b = string))

mouse_points = [(86, 299), (1050, 299)]
mouse_points_button = [(300, 386), (1260, 386)]

async def enter_key(key, slot = 0):
    df=pd.DataFrame([key])
    df.to_clipboard(index=False,header=False)
    pyautogui.moveTo(mouse_points[slot][0], mouse_points[slot][1], duration=0.1)
    pyautogui.click(mouse_points[slot][0], mouse_points[slot][1], button=pyautogui.LEFT)
    pyautogui.hotkey('ctrl', 'v')
    await asyncio.sleep(0.05)
    pyautogui.press("enter")

async def frame_event(img):
        if ip.is_givaway(img, (6.407418514812385, 5.406766752083711, 63.57950020636679), 3):
            keys = ip.get_text(img).splitlines()
            slot = 0
            for i in keys:
                if len(i) == 29:
                    if not i in detected_keys:
                        log("Key: " + i)
                        detected_keys.append(i)
                        enter_key(i, slot)
                        slot += 1
        log("Failed Detecton Code")


            # File has changed, so do something...

async def main():
    log("Starting Video Streamer")
    stream = VideoStreamer("https://www.twitch.tv/neutrinogreen")
    log("Enterning Main Loop")
    while True:
        frame = stream.read()
        cv2.imwrite("out.jpeg", frame)
        loop.create_task(frame_event(frame))
        await asyncio.sleep(0.05)



if __name__ == "__main__":
    
    log("Starting KeyBot")
    log("Starting Async Event Loop")
    loop.create_task(main())
    loop.run_forever()


