function init(){
	window.canvas = document.getElementById('graph')
	var artistapi = new createXHR(parseartist);
	artistapi.xhr.open('GET','http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist='+artistName+'&api_key=cfd308fec04046d826ca5806015a529a&format=json',false);
	artist.api.xhr.send();
}
function parseartist(data){
	var icon = //whatever the JSON name for lg icon is, I CAN'T ACCESS THE API THROUGH THE RED CLAY PROXY
}
function createXHR(callback){
	this.callback = callback;
	if (window.XMLHttpRequest){
    	this.xhr = new XMLHttpRequest();
	} else if (window.ActiveXObject){
    	this.xhr = new ActiveXObject("Microsoft.XMLHTTP");
	} else{
		alert('I can\'t seem to find a way to send an XHR!');
	};
	that = this;
	this.xhr.onload = function(){
		that.callback.call(this,eval(that.xhr.responseText));
	};
};
init()