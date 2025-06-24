#Standard
import math,time,random

#Internet stuff
import asyncio,websockets
import webbrowser

#Filesystem stuff
import glob,os

#Image processing stuff
from PIL import Image
import numpy as np
import cv2

#Basic warnings
from warnings import warn

#Ascii contrast scale, in ascending order
SCALE = ' .\'`^",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'

#Server on localhost
HOST = "127.0.0.1"
PORT = 8080

#Duration is a global so it can be set from one socket session to the next
global duration

def gif_to_frames(gif_path, output_dir="_frames"):
    #Function to turn a gif into individual frames

    try: #overengineered, especially since I pass it results of a glob search fo gifs
        gif = Image.open(gif_path) #Actually open the file
    except FileNotFoundError:
        print(f"Error: GIF file not found at {gif_path}")
        return

    try: #moderately overengineered, gifs usually have data in them.
        gif.seek(0)  # Go to the first frame
    except EOFError:
        print("Error: GIF has no frames")
        return

    #Iterate over the frames
    frame_num = 0
    while True: #loop until break, kind of gross, where'd I get this?
        try:
            frame = gif.copy()  # Make a copy to avoid modifying the original GIF
            frame.save(f"{output_dir}/frame_{frame_num:03d}.png")  # Save as PNG
            frame_num += 1
            gif.seek(gif.tell() + 1)  # Move to the next frame
        except EOFError: #Kludgy... did an AI write this?
            break  # Exit loop when no more frames

    #Output lets us get the duration later.
    return gif

def grab_a_pic(index):
    #Function to grab a single image at an index
    # Could probably just glob for the one number, but this feels more comprehensive. Still might change later.

    files = glob.glob("_frames/*.png") #go get the files 
    files.sort(key=lambda x:int(x.split("/")[-1].split("_")[-1].split(".")[0])) #sort them in asecnding oeder
    fil = files[index%len(files)] #Grab the index-th frame
    print(fil) #A little output- diagnostic
    img_sp = cv2.imread(fil) #Pull the image in
    return asciify(img_sp) #spit it back out asciified

def asciify(img,eqHist=False):
    #Convert an image to an ascii-graphics form

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert to grasyscale- color version is absurdly slow

    if eqHist: #Optional param to equalize, helps with contrast, sometimes
        gray = cv2.equalizeHist(gray)

    #Grab the shape and resize the image to match the 5:3 ratio of <pre> text
    sx,sy = np.shape(gray)
    maxS = max([sx,sy])
    rsz = 67.0/maxS #max side set to 67 so the max dimension will be 200
    img_sm = cv2.resize(gray,(int(5*rsz*sy),int(3*rsz*sx)))
    img_ascale = np.astype((len(SCALE)-1)*(img_sm/255.0),np.uint8) #Re-fit the intensities to the length of the ASCII contrast scale

    ascii_op = "" #make the output string
    sx,sy = np.shape(img_sm) #Get the final shape
    for i in range(sx): #Loop over x and y
        for j in range(sy):
            ascii_op = ascii_op + SCALE[img_ascale[i][j]] #Add in the corresponding indexed ascii level
        ascii_op = ascii_op + "<br/>" #Add a break after each row

    #Return the final string
    return ascii_op

async def handle_client(websocket):
    #Server handler function

    global duration #grab the duration, if it's set

    try: #For an unbroken connection
        async for message in websocket: #For each message
            print(message) #Received display- diagnostic

            if duration != None: #If the duration hasn't been sent yet
                msg =  '§' + str(duration) #Send the duration with the delimiter
                duration = None #note that the duration has been sent
            else: #Otherwise
                msg = grab_a_pic(int(message)) #Send out the next asciified frame
            await websocket.send(msg) #Send the message
    #Do nothing when the connection breaks
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    #Main run 

    global duration #Global duration is set here
    
    prev_fs = glob.glob("_frames/*") #Grab any frames from last run
    for f in prev_fs:
        os.remove(f) #Remove them all

    g_imgs = glob.glob("*.gif") #Grab the new gif

    if len(g_imgs)>0: #If there's a gif to be grabbed
        gifImage = g_imgs[0] #grab it
        gif = gif_to_frames(gifImage) #make the individual framed
        duration = gif.info['duration'] #snag the duration

        #Prep the server
        server = await websockets.serve(handle_client, HOST, PORT)
        webbrowser.open("anim.html") #Open the html/js side in the browser
        await server.wait_closed() #fire up the server
    else:
        warn("NO GIF!") #Oops, you forgot the gif!

if __name__ == "__main__":
    #do thing
    asyncio.run(main())
    
