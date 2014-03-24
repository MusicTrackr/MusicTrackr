import sendgrid
import json
import urllib.request
from flask import Flask, request, render_template
from ast import literal_eval
#HELLYEAH
app = Flask(__name__)

def init():
	global githuburl = 'https://www.github.com/kaikue/MusicAlert'
	try:
		artistf = open('artists.txt','r')
		afcontents = literal_eval(artistf.read().strip())
		artistf.close()
	except IOError:
		artistf = open('artists.txt','x')
		artistf.close()
		afcontents = ''
	if type(afcontents) is dict:
		global artists = afcontents
	else:
		print('Artists file empty. Running with empty dict..')
		global artists = {}
	app.run(debug=True)

def subscribe(artist_name, email):
	id = get_artist_id(artist_name)
	if id not in artists.keys():
		artists[id] = {"subscribers":[], "albums":get_albums(id)}
	if email not in artists[id]['subscribers']:
		artists[id]['subscribers'].append(email)
	artistf.write(str(artists))
	if 'testing' in globals() and testing is True:
		artists[get_artist_id(artist_name)]["albums"].pop(0)
		update()

def update():
	#run this every morn
	for artist in artists:
		old_albums = artists[artist]['albums']
		new_albums = get_albums(artist)
		for new_album in new_albums:
			if new_album not in old_albums:
				for subscriber in artists[artist]['subscribers']:
					mailuser(subscriber, new_album['artistName'], new_album['collectionName'], new_album['collectionViewUrl'])
		artists[artist]['albums'] = new_albums
	artistf.write(str(artists))

def get_json(url):
	page = urllib.request.urlopen(url)
	return json.loads(page.read().decode(page.headers.get_content_charset()))

def get_artist_id(name):
	#from input get artist id
	plus_name = name.replace(" ", "+")
	dat = get_json("https://itunes.apple.com/search?term=" + plus_name)
	for i in range(0,len(dat['results'])-1):
		if dat["results"][i]["artistName"].lower() == name.lower():
			artistId = dat['results'][i]['artistId']
			break
	return artistId

#from artist id get albums
def get_albums(id):
	#id is a string
	albums = []
	dat = get_json("https://itunes.apple.com/lookup?id=" + id + "&entity=album")
	for result in dat["results"]:
		if result["wrapperType"] == "collection":
			del result['copyright']
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
	print("Mailed user with status " + str(status))

@app.route('/',methods=['GET','POST'])
def form():
	page = 'Home'
	if request.method == 'POST':
		try:
			if 'test(' in request.form['email']:
				global testing
				testing = True
				email = request.form['email'][len('test('):len(request.form['email'])-1]
				print('test')
				print(email)
				subscribe(request.form['artist'],email)
				result = 'You successfully subscribed to that artist.'
			elif request.form['email'].replace(' ','') = '':
				result = 'Please enter a search term.'
			else:
				subscribe(request.form['artist'],request.form['email'])
				result = 'You successfully subscribed to that artist.'
		except Exception as e:
			result = 'Sorry, your request could not be completed. ' + '<br/>' + 'The error returned was: ' + str(e) + '<br/><a href="{{githuburl}}/issues">Report this error</a>'
		return render_template('index.html',result=result)
	return render_template('index.html')

'''@app.route('/artists.txt')
def artiststxt():
	artistf.write(str(artists))
	return artistf.read()'''

if __name__ == '__main__':
	init()