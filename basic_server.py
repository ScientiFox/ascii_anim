import math,time,random

import asyncio,websockets
import webbrowser
import glob
import numpy as np
import cv2

SCALE = ' .\'`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

HOST = "127.0.0.1"
PORT = 8080

bwr_open = False

i_time = time.time()

def grab_a_pic(index):
    files = glob.glob("_frames/*.png")
    files.sort(key=lambda x:int(x.split("/")[-1].split("_")[-1].split(".")[0]))
    fil = files[index%len(files)]
    print(fil)
    img_sp = cv2.imread(fil)
    return asciify(img_sp)

def asciify(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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

    try:
        async for message in websocket:
            print(message)
            msg = grab_a_pic(int(message))
            await websocket.send(msg)

    except websockets.exceptions.ConnectionClosed:
        pass

async def main():

    server = await websockets.serve(handle_client, HOST, PORT)

    webbrowser.open("websocket_test.html")

    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
    
