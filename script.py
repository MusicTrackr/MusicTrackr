import sendgrid
import json
artists = {}
def init():
	artistf = open('artists.txt','r+')
	artists = artistf.read().strip()
	#print(artists)
	main()
def main():
	'''while True:
		for artist in artists:
			for subscriber in artist['subscribers']:
				if artist['newalbum'] is not False:
					mailuser(subscriber['email'],artist,newalbum)'''
#def mailuser(address,artist,newalbum):
	#TODO
init()