This is a little project for fun that animates an ascii gif in a browser window.

It's a python server that opens up a gif, partitions it into individual images, converts those to ACSII levels, and then sends those over to a JS script in the browser that displays them, synced with their original gif duration.

Execution just requires a gif in the same directory as the server. Running the server fires up the browser and runs the JS there.
