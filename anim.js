//Basic timer variables
let clock,i_time;

//Clock initialization
d = new Date();
i_time = d.getTime();
clock = 0 //d.getTime()-i_time;

//Variable to hold incoming messages
let WSmessage;
WSmessage = "";

//Open the connection
sock = new WebSocket('ws://127.0.0.1:8080');

//Set the websocket callbacks
sock.onopen = function(event){setElement("state","opened");};
sock.onmessage = function(event){WSmessage=event.data;};
sock.onclose = function(event){setElement("state","closed");};

//start up image timer settings
let im_timer,im_per,i_ct;
i_ct = 0;
im_timer = d.getTime();
im_per = 50;

//Main Loop.
setInterval(tickTock,10);

//redundant helper function to set an element. Why did I do this?
function setElement(id,value){document.getElementById(id).innerHTML=value;}

//Call to the server- sends an index, which sets the frame to be processed and sent
function makeCall(){sock.send(i_ct);}

//main function
function tickTock(){

	//Update the timer
	d = new Date();
	clock = d.getTime()-i_time;

	//Check if it's been the length of time set by the gif duration, and less than the 1200 frame max
	if ((d.getTime()-im_timer>im_per)&&(i_ct<1200)){
		im_timer = d.getTime();	//Reset the timer
		makeCall(); //Send the counter to the server
		i_ct=i_ct+1; //Increase the frame cycle counter
	}

	//we're using the paragraph symbol as a delimiter since it's rare and won't show up in the ascii image
	if (WSmessage[0] == '§'){ //It transmits the per-frame duration of the gif
		perString = ''; //string to hold the actual time value
		i = 1;
		//loop through the message and extract everything not the delimiter
		while (i < WSmessage.length){perString = perString + WSmessage[i];i=i+1;}
		im_per = parseInt(perString); //Turn all that into an int
	}
	else{ //If it's not got the delimiter, it's just an image frame, pop it on screen
		setElement("data",WSmessage);
	}
}

