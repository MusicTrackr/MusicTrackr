import sendgrid

RECEPIENT = "emailforspam.spammeplease@gmail.com"
ARTIST = "Skrillex"
ALBUM_LINK = "http://google.com"

s = sendgrid.SendGridClient('parasm', 'bcabooks')
msg = sendgrid.Mail()
msg.add_to(RECEPIENT)
msg.set_subject("MusicTrackr: New Album Release")
msg.set_html("A new album has been released by " + "! Find it on <a href=\"" + ALBUM_LINK + "\">iTunes</a>.")
msg.set_from("notif@musictrackr.com")
status, msg = s.send(message)