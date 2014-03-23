import sendgrid
import json
import urllib.request
from sys import argv, exit
from ast import literal_eval
from flask import Flask, request, render_template
#HELLYEAH
testing = False
app = Flask(__name__)
artists = {} #ids to subscribers, albums

def subscribe(artist_name, email):
	id = get_artist_id(artist_name)
	if id not in artists.keys():
		artists[id] = {"subscribers":[], "albums":get_albums(id)}
	if email not in artists[id]['subscribers']:
		artists[id]['subscribers'].append(email)
	print(artists[id]["subscribers"])

def update():
	#run this every morn
	for artist in artists:
		old_albums = artists[artist]['albums']
		new_albums = get_albums(artist)
		for new_album in new_albums:
			if new_album not in old_albums:
				for subscriber in artists[artist]['subscribers']:
					if testing is False:
						mailuser(subscriber, new_album['artistName'], new_album['collectionName'], new_album['collectionViewUrl'])
		artists[artist]['albums'] = new_albums

def get_json(url):
	page = urllib.request.urlopen(url)
	return json.loads(page.read().decode(page.headers.get_content_charset()))

def get_artist_id(name):
	#from input get artist id
	plus_name = name.replace(" ", "+")
	dat = get_json("https://itunes.apple.com/search?term=" + plus_name)
	i = 0
	while dat["results"][i]["artistName"].lower() != name.lower():
		i += 1
	return str(dat["results"][i]["artistId"])

#from artist id get albums
def get_albums(id):
	#id is a string
	albums = []
	dat = get_json("https://itunes.apple.com/lookup?id=" + id + "&entity=album")
	for result in dat["results"]:
		if result["wrapperType"] == "collection":
			albums.append(result)
	return albums

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

def test():
	subscribe("Skrillex", 'ezra.m.brooks@gmail.com')
	artists[get_artist_id("Skrillex")]["albums"].pop(0)
	update()

if 'argv' in globals():
	if 'cron' in argv:
		update()
		exit(0)
	if 'test' in argv:
		testing = True
		exit(0)

@app.route('/',methods=['GET','POST'])
def formtest():
	test()
	if request.method == 'POST':
		subscribe(request.form['testinput'],'ezra.m.brooks@gmail.com')
		result = 'success'
		return render_template('index.html',result=result)
	return render_template('index.html')
if __name__ == '__main__':
	app.run(debug=True)