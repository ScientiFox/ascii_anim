
let clock,i_time;

d = new Date();
i_time = d.getTime();
clock = 0 //d.getTime()-i_time;

let WSmessage;
WSmessage = "";

sock = new WebSocket('ws://127.0.0.1:8080');

sock.onopen = function(event){setElement("state","opened");};
sock.onmessage = function(event){WSmessage=event.data;};
sock.onclose = function(event){setElement("state","closed");};

let im_timer,im_per,i_ct;
i_ct = 0;
im_timer = d.getTime();
im_per = 50;

//Main Loop.
setInterval(tickTock,10);

function setElement(id,value){
	document.getElementById(id).innerHTML=value;
}

function makeCall(){
	sock.send(i_ct); //"client clocktime is: "+(clock/1000.0)+"s"
}

function tickTock(){

	d = new Date();
	clock = d.getTime()-i_time;
	//document.getElementById('clock').innerHTML="Clocktime: "+(clock/1000.0)+"s";

	if ((d.getTime()-im_timer>im_per)&&(i_ct<1200)){
		im_timer = d.getTime();
		makeCall();
		i_ct=i_ct+1;
	}

	if (WSmessage[0] == '§'){
		perString = '';
		i = 1;
		while (i < WSmessage.length){perString = perString + WSmessage[i];i=i+1;}
		im_per = parseInt(perString);
		//alert(im_per);
	}
	else{
		setElement("data",WSmessage);
	}

}

