MusicTrackr
==
Notifies you when your favorite artists release a new album.  
Made at hackBCA by Kai Kuehner, Ryan Seffinger, Ryan Stillings, and Ezra Brooks.  
Depends upon [sendgrid-python](https://www.github.com/sendgrid/sendgrid-python) and [Flask](https://www.github.com/mitsuhiko/flask).  
Procfile and requirements.txt provided for deployment to [Heroku](https://www.heroku.com) with a GUnicorn web server.  
APIs Used
--
 - iTunes Search
 - SendGrid
 - last.fm  
  
###Example lastfmkey.json  
This project requires a last.fm API key/account for certain artist-tracking functions. Drop a file like this into static/lastfmkey.json:  
```json
{
	"apikey":"your_api_key_here",
	"apisecret":"your_api_secret_here"
}
```
  
In reality, nobody's sure why you would ever use MusicTrackr for any artist other than Skrillex. And by "nobody," we mean "anyone who isn't [Kai](https://www.github.com/kaikue)."