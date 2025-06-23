import math,time,random

import asyncio,websockets
import webbrowser

import glob,os

from PIL import Image
import numpy as np
import cv2

from warnings import warn

SCALE = ' .\'`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

HOST = "127.0.0.1"
PORT = 8080

bwr_open = False

global duration

def gif_to_frames(gif_path, output_dir="_frames"):

    try:
        gif = Image.open(gif_path)
    except FileNotFoundError:
        print(f"Error: GIF file not found at {gif_path}")
        return

    try:
        gif.seek(0)  # Go to the first frame
    except EOFError:
        print("Error: GIF has no frames")
        return

    frame_num = 0
    while True:
        try:
            frame = gif.copy()  # Make a copy to avoid modifying the original GIF
            frame.save(f"{output_dir}/frame_{frame_num:03d}.png")  # Save as PNG
            frame_num += 1
            gif.seek(gif.tell() + 1)  # Move to the next frame
        except EOFError:
            break  # Exit loop when no more frames

    return gif

def grab_a_pic(index):
    files = glob.glob("_frames/*.png")
    files.sort(key=lambda x:int(x.split("/")[-1].split("_")[-1].split(".")[0]))
    fil = files[index%len(files)]
    print(fil)
    img_sp = cv2.imread(fil)
    return asciify(img_sp)

def asciify(img,eqHist=False):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if eqHist:
        gray = cv2.equalizeHist(gray)

    sx,sy = np.shape(gray)
    maxS = max([sx,sy])
    rsz = 67.0/maxS
    img_sm = cv2.resize(gray,(int(5*rsz*sy),int(3*rsz*sx)))
    img_ascale = np.astype((len(SCALE)-1)*(img_sm/255.0),np.uint8)

    ascii_op = ""
    sx,sy = np.shape(img_sm)
    for i in range(sx):
        for j in range(sy):
            ascii_op = ascii_op + SCALE[img_ascale[i][j]]
        ascii_op = ascii_op + "<br/>"

    return ascii_op

async def handle_client(websocket):

    global duration

    try:
        async for message in websocket:
            print(message)

            if duration != None:
                msg =  '§' + str(duration)
                duration = None
            else:
                msg = grab_a_pic(int(message))
            await websocket.send(msg)

    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    global duration
    
    prev_fs = glob.glob("_frames/*")
    for f in prev_fs:
        os.remove(f)

    g_imgs = glob.glob("*.gif")

    if len(g_imgs)>0:
        gifImage = g_imgs[0]
        gif = gif_to_frames(gifImage)
        duration = gif.info['duration']

        server = await websockets.serve(handle_client, HOST, PORT)
        webbrowser.open("anim.html")
        await server.wait_closed()
    else:
        warn("NO GIF!")

if __name__ == "__main__":
    asyncio.run(main())
    
