import sendgrid
import json
import requests

artists = {}

def init():
	artistf = open('artists.txt','r+')
	artists = artistf.read().strip()
	#print(artists)
	main()

def get_artist_id(name):
	#from input get artist id
	name = name.replace(" ", "+")
	page = requests.get("https://itunes.apple.com/search?term=" + name)
	txt = page.text
	print(txt)
	dat = json.loads(txt)
	return dat["results"][0]["artist_id"]

#from artist id get albums


def main():
	'''while True:
		for artist in artists:
			for subscriber in artist['subscribers']:
				if artist['newalbum'] is not False:
					mailuser(subscriber['email'],artist,newalbum)'''

def mailuser(address, artist, newalbum):
	#address: email address (string)
	#artist: artist's name (string)
	#newalbum: link to new album (string)
	s = sendgrid.SendGridClient('parasm', 'bcabooks')
	msg = sendgrid.Mail()
	msg.add_to(address)
	msg.set_subject("MusicTrackr: New Album Release")
	msg.set_html("A new album has been released by " + artist + "! Find it on <a href=\"" + newalbum + "\">iTunes</a>.")
	msg.set_from("notif@musictrackr.com")
	status, msg = s.send(message)

init()