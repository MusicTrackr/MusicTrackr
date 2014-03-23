import sendgrid
import json
import urllib.request
from sys import argv

artists = {}

def init():
	artistf = open('artists.txt','r+')
	artists = artistf.read().strip()
	#print(artists)
	main()

artists_albums = {}
artists_subscribers = {}

def subscribe(artist_name, email):
	id = get_artist_id(artist_name)
	if id not in artists_subscribers.keys():
		artists_subscribers[id] = [email]
	else:
		artists_subscribers[id].append(email)

def update():
	#run this every morn
	for artist in artists_albums.keys():
		old_albums = artists_albums[artist]
		new_albums = get_albums(artist)
		for new_album in new_albums:
			if new_album not in old_albums:
				for subscriber in artists_subscribers[artist]:
					mailuser(subscriber, new_album[artistName], new_album[collectionName], new_album[collectionViewUrl])
		artists_albums[artist] = new_albums

def get_json(url):
	page = urllib.request.urlopen(url)
	txt = page.read().decode(page.headers.get_content_charset())
	dat = json.loads(txt)
	return dat

def get_artist_id(name):
	#from input get artist id
	name = name.replace(" ", "+")
	dat = get_json("https://itunes.apple.com/search?term=" + name)
	return dat["results"][0]["artistId"]

#from artist id get albums
def get_albums(id):
	#id is a string
	albums = []
	dat = get_json("https://itunes.apple.com/lookup?id=" + id + "&entity=album")
	for result in dat["results"]:
		if result["wrapperType"] == "collection":
			albums.append(result)
	return albums

def main():
	'''while True:
		for artist in artists:
			for subscriber in artist['subscribers']:
				if artist['newalbum'] is not False:
					mailuser(subscriber['email'],artist,newalbum)'''

def mailuser(address, artist, album, url):
	#address: email address (string)
	#artist: artist's name (string)
	#album: name of album (string)
	#url: link to album (string)
	s = sendgrid.SendGridClient('parasm', 'bcabooks')
	msg = sendgrid.Mail()
	msg.add_to(address)
	msg.set_subject("MusicTrackr: New Album Release")
	msg.set_html("A new album, " + album + ", has been released by " + artist + "! Find it on <a href=\"" + url + "\">iTunes</a>.")
	msg.set_from("notif@musictrackr.com")
	status, msg = s.send(msg)

if 'argv' in globals():
	if 'cron' in argv:
		update()
	else:
		init()
else:
	init()