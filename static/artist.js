function init(){
	var canvas = document.getElementById('graph').getContext('2d')
	var artistapi = new createXHR(parseartist);
	artistapi.xhr.open('GET','http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist='+artistName.replace(' ','+')+'&api_key=cfd308fec04046d826ca5806015a529a&format=json',false);
	artistapi.xhr.send();
}
function parseartist(data){
	var artist = {
		icon: //whatever the JSON name for log icon is, I CAN'T ACCESS THE API THROUGH THE RED CLAY PROXY
		plays: //see above
	}
	document.getElementById('plays').innerHTML = artist.plays
}
function createXHR(callback){
	this.callback = callback;
	if (window.XMLHttpRequest){
    	this.xhr = new XMLHttpRequest();
	} else if (window.ActiveXObject){
    	this.xhr = new ActiveXObject("Microsoft.XMLHTTP");
	} else{
		alert('Can\'t find a way to send an XHR!');
	};
	that = this;
	this.xhr.onload = function(){
		that.callback.call(this,eval(that.xhr.responseText));
	};
};
init()