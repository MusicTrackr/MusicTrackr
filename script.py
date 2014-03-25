#builtins
import json
import urllib.request
from urllib.error import URLError
from datetime import datetime, timedelta
from ast import literal_eval
from threading import Timer
#dependencies
import sendgrid
from flask import Flask, request, render_template
#HELLYEAH
app = Flask(__name__)

def init():
	global githubUrl
	global artistf
	global artists
	githubUrl = 'https://www.github.com/kaikue/MusicAlert'
	try:
		artistf = open('artists.txt','r+')
		artists = literal_eval(artistf.read().strip())
	except (SyntaxError,ValueError,TypeError):
		print('Literal_eval error.')
		artistf = open('artists.txt','w+')
		artists = {}
	except FileNotFoundError:
		artistf = open('artists.txt','w+')
		artists = {}
	if artists == {}:
		print('Artists file empty or corrupt. Running with empty dict..')
	today = datetime.today()
	t = Timer(timedelta(days=1,hours=-today.hour,minutes=-today.minute,seconds=-today.second,microseconds=-today.microsecond).total_seconds(),update)
	t.start()
	app.run(debug=True)

def subscribe(artistName, email):
	id = getArtistId(artistName)
	if id not in artists.keys():
		artists[id] = {"subscribers":[], "albums":getAlbums(id)}
	if email not in artists[id]['subscribers']:
		artists[id]['subscribers'].append(email)
	if 'testing' in globals() and testing is True:
		artists[getArtistId(artistName)]["albums"].pop(0)
		update()
	else:
		artistf.truncate()
		artistf.write(str(artists))

def update():
	#run this every morn
	for artist in artists:
		oldAlbums = artists[artist]['albums']
		newAlbums = getAlbums(artist)
		for newAlbum in newAlbums:
			if newAlbum not in oldAlbums:
				for subscriber in artists[artist]['subscribers']:
					mailUser(subscriber, newAlbum['artistName'], newAlbum['collectionName'], newAlbum['collectionViewUrl'])
		artists[artist]['albums'] = newAlbums
	artistf.truncate()
	artistf.write(str(artists))
	t = Timer(timedelta(days=1,hours=-today.hour,minutes=-today.minute,seconds=-today.second,microseconds=-today.microsecond).total_seconds(),update)
	t.start()

def getJson(url):
	page = urllib.request.urlopen(url)
	return json.loads(page.read().decode(page.headers.get_content_charset()))

def getArtistId(name):
	#from input get artist id
	plusName = name.replace(" ", "+")
	dat = getJson("https://itunes.apple.com/search?term=" + plusName + '&entity=musicArtist')
	for i in range(0,len(dat['results'])-1):
		if dat["results"][i]["artistName"].lower() == name.lower():
			artistId = dat['results'][i]['artistId']
			return artistId

#from artist id get albums
def getAlbums(id):
	#id is NOT a string
	albums = []
	dat = getJson("https://itunes.apple.com/lookup?id=" + str(id) + "&entity=album")
	for result in dat["results"]:
		if result["wrapperType"] == "collection":
			del result['copyright']
			albums.append(result)
	return albums

def mailUser(address, artist, album, url):
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
	print("Mailed user with status " + str(status))

@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'POST':
		try:
			if 'test(' in request.form['email']:
				global testing
				testing = True
				email = request.form['email'][len('test('):len(request.form['email'])-1]
				print('test')
				print(email)
				subscribe(request.form['artist'],email)
				success = 'You successfully subscribed to that artist.'
				error = None
			elif request.form['email'].replace(' ','') == '' or request.form['email'].find('@') == -1 or request.form['email'][request.form['email'].find('@'):len(request.form['email'])-1].find('.') == -1:
				error = 'Please enter a valid email address.'
				success = None
			elif request.form['artist'].replace(' ','') == '':
				error = 'Please enter a valid artist.'
				success = None
			else:
				subscribe(request.form['artist'],request.form['email'])
				success = 'You successfully subscribed to that artist.'
				error = None
		except URLError:
			error = 'Sorry, we couldn\'t find data on the artist you entered.'
			success = None
		except Exception as e:
			print(str(e))
			error = 'Sorry, your request could not be completed. The error returned was: ' + str(e)
			success = None
		return render_template('index.html',error=error,success=success)
	return render_template('index.html')

'''@app.route('/artists.txt')
def artiststxt():
	artistf.truncate()
	artistf.write(str(artists))
	artistf.flush()
	afcontents = artistf.read()
	return afcontents'''

@app.route('/artist')
def artistPage():
	artistName = request.args['artist']
	print(artistName)
	return render_template('index.html') #just don't 404 bro

if __name__ == '__main__':
	init()